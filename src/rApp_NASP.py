import argparse
import json
import logging
import requests
import yaml
import uuid
import sys
from tools import extract_flow_bit_rate, to_prb

from flask import Flask, request, jsonify
from rApp_catalogue_client import rAppCatalogueClient

DEFAULT_CONFIG_FILE_PATH = "src/config/config.yaml"


def setup_logging(config):
    """
    Configures logging settings for the application.

    Args:
        config (dict): Configuration settings including the desired logging level.

    Returns:
        logging.Logger: Configured logger instance.
    """
    level = config.get('logging', {}).get('level', 'INFO').upper()  # Default to INFO if not specified
    numeric_level = getattr(logging, level, None)
    if not isinstance(numeric_level, int):
        raise ValueError(f'Invalid log level: {level}')
    logging.basicConfig(level=numeric_level, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)


def parse_arguments():
    """
    Parses command line arguments specific to the rApp NASP.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description='RIC Optimizer arguments.')
    parser.add_argument('-c', '--config', type=str, default=DEFAULT_CONFIG_FILE_PATH,
                        help='Path to the configuration file.')
    return parser.parse_args()


class NASPPolicy:
    def __init__(self, config, logger):
        self.config = config
        self.slice_policy = {}
        self.e2nodelist = []
        self.logger = logger

    def fill_policy_body(self, config, data):
        """
        Fills the policybody dictionary with the required values from the configuration and data.

        Args:
            config (dict): Configuration settings.
            data (list): List of E2 nodes.

        Returns:
            dict: Filled policybody dictionary.
        """
        e2_node_list = []

        for node in data:
            # Prepare RRMPolicyRatioList for each node
            rrm_policy_ratio_list = []
            if "RRMPolicyRatioList" in node:
                for policy in node["RRMPolicyRatioList"]:
                    rrm_policy_ratio = {
                        "plmnid": policy["plmnid"],
                        "sst": policy["sst"],
                        "sd": policy["sd"],
                        "minPRB": policy["minPRB"],
                        "maxPRB": policy["maxPRB"]
                    }
                    rrm_policy_ratio_list.append(rrm_policy_ratio)

            e2_node = {
                "mcc": node["mcc"],
                "mnc": node["mnc"],
                "e2nodeid": node["e2nodeid"],
                "RRMPolicyRatioList": rrm_policy_ratio_list
            }
            e2_node_list.append(e2_node)

        policybody = {
            "ric_id": config['nonrtric']['ric_id'],
            "policy_id": str(uuid.uuid4()),
            "service_id": config['nonrtric']['service_name'],
            "policy_data": {"E2NodeList": e2_node_list},
            "policytype_id": config['nonrtric']['policytype_id'],
        }

        self.slice_policy = policybody

        self.logger.debug('Policy body: %s', json.dumps(self.slice_policy, indent=2))
        return self.slice_policy

    def put_policy(self, body):
        """
        Sends a PUT request to create a policy.

        Args:
            body (dict): The JSON body of the request.

        Returns:
            bool: True if the policy is created successfully, False otherwise.
        """
        complete_url = self.config['nonrtric']['base_url_pms'] + "/policies"
        headers = {"content-type": "application/json"}
        self.logger.debug(f"Sending PUT request to {complete_url} with body: {json.dumps(body, indent=2)}")
        try:
            resp = requests.put(complete_url, json=body, headers=headers, verify=False)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Failed to create policy. Error: {e}")
            return False
        else:
            self.logger.info("Policy created successfully.")
            return True

    def create_policy(self, e2_node_data):
        """
        Creates and posts a policy based on provided E2 node data.

        Args:
            e2_node_data (list): List of E2 nodes.

        Returns:
            dict: Result message with status.
        """
        policy = self.fill_policy_body(self.config, e2_node_data)
        success = self.put_policy(policy)
        if success:
            return {"status": "success", "message": "Policy created successfully."}
        else:
            return {"status": "failure", "message": "Failed to create policy."}

    def load_e2nodelist(self):
        """
        Loads E2 node list from a data source. Currently a stub method returning example data.

        Returns:
            list: List of E2 nodes.
        """
        # Mocked data for example purposes
        self.e2nodelist = [
            {
                "mcc": "001",
                "mnc": "01",
                "e2nodeid": "node123",
                "RRMPolicyRatioList": [
                    {"plmnid": "00101", "sst": 1, "sd": 1, "minPRB": 10, "maxPRB": 20}
                ]
            }
        ]
        self.logger.debug("E2 node list loaded: %s", json.dumps(self.e2nodelist, indent=2))
        return self.e2nodelist

    def run(self):
        """
        Executes the policy creation process.
        """
        self.logger.info('Running the NASP rAPP.')
        self.logger.debug('Configuration: %s', json.dumps(self.config, indent=2))
        self.load_e2nodelist()
        policy = self.fill_policy_body(self.config, self.e2nodelist)
        self.put_policy(policy)


def create_app(config, logger):
    """
    Creates and configures the Flask application.

    Args:
        config (dict): Configuration settings.
        logger (logging.Logger): Configured logger.

    Returns:
        Flask: Configured Flask application.
    """
    app = Flask(__name__)

    # Initialize NASPPolicy instance
    nasp_policy = NASPPolicy(config, logger)

    @app.route('/create_slice_policy', methods=['POST'])
    def create_slice_policy():
        """
        API endpoint to create and post a policy based on received JSON data.

        Expects JSON data with E2 node information.

        Returns:
            JSON response indicating success or failure.
        """
        if not request.is_json:
            logger.warning("Received non-JSON request.")
            return jsonify({"status": "failure", "message": "Request must be in JSON format."}), 400

        data = request.get_json()
        logger.debug(f"Received data: {json.dumps(data, indent=2)}")

        downlink_min, downlink_max = extract_flow_bit_rate(data)
        logger.debug(f"Downlink min: {downlink_min}, Downlink max: {downlink_max}")
        downlink_min_prb = to_prb(downlink_min, False, 28, 1, 50, is_tdd=False)
        downlink_max_prb = to_prb(downlink_max, False, 28, 1, 50, is_tdd=False)
        logger.debug(f"Downlink min PRB: {downlink_min_prb}, Downlink max PRB: {downlink_max_prb}")
        # Validate input data
        if not isinstance(data, list):
            logger.error("Invalid data format. Expected a list of E2 nodes.")
            return jsonify({"status": "failure", "message": "Invalid data format. Expected a list of E2 nodes."}), 400

        # Optionally, add more validation for each node's required fields

        result = nasp_policy.create_policy(data)
        if result["status"] == "success":
            return jsonify(result), 201
        else:
            return jsonify(result), 500

    app.route('/create_slice_policy', methods=['POST'])(create_slice_policy)

    return app


if __name__ == "__main__":
    args = parse_arguments()

    # Load the configuration from the file
    try:
        with open(args.config, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Configuration file not found: {args.config}")
        sys.exit(1)
    except yaml.YAMLError as exc:
        print(f"Error parsing configuration file: {exc}")
        sys.exit(1)

    # Now set up logging according to config
    logger = setup_logging(config)
    logger.debug("Configuration loaded successfully.")

    register = rAppCatalogueClient(args.config)

    if register.register_service():
        logger.info("Service successfully registered on rApp catalogue.")
    else:
        logger.error("Failed to register service.")
        sys.exit(1)

    # Retrieve API server configurations from config file
    api_config = config.get('api_server', {})
    host = api_config.get('host', '0.0.0.0')  # Default to '0.0.0.0' if not specified
    port = api_config.get('port', 5000)       # Default to 5000 if not specified

    # Create Flask app
    app = create_app(config, logger)

    # Run Flask app
    try:
        logger.info(f"Starting API server at {host}:{port}")
        app.run(host=host, port=port)
    except Exception as e:
        logger.error(f"Failed to start API server: {e}")
        sys.exit(1)