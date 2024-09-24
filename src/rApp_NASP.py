import argparse
import json
import logging
import requests
import yaml
import uuid
import sys

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
    Parses command line arguments specific to the rAPp NASP.

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

        # Create the policy body with the processed E2NodeList
        policybody = {
            "ric_id": config['nonrtric']['ric_id'],
            "policy_id": str(uuid.uuid4()),
            "service_id": config['nonrtric']['service_name'],
            "policy_data": {"E2NodeList": e2_node_list},
            "policytype_id": config['nonrtric']['policytype_id'],
        }

        self.slice_policy = policybody

        logger.debug('Policy body: %s', json.dumps(self.slice_policy, indent=2))
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
        logger.debug(f"Sending PUT request to {complete_url} with body: {json.dumps(body, indent=2)}")
        try:
            resp = requests.put(complete_url, json=body, headers=headers, verify=False)
            resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to create policy. Error: {e}")
            return False
        else:
            logger.info("Policy created successfully.")
            return True

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
        logger.debug("E2 node list loaded: %s", json.dumps(self.e2nodelist, indent=2))
        return self.e2nodelist

    def run(self):
        """
        Executes the policy creation process.
        """
        logger.info('Running the NASP rAPP.')
        logger.debug('Configuration: %s', json.dumps(self.config, indent=2))
        self.load_e2nodelist()
        policy = self.fill_policy_body(self.config, self.e2nodelist)
        self.put_policy(policy)


if __name__ == "__main__":
    args = parse_arguments()

    # Load the configuration from the file
    try:
        with open(args.config, 'r') as file:
            config = yaml.safe_load(file)
    except FileNotFoundError:
        sys.exit(1)
    except yaml.YAMLError as exc:
        sys.exit(1)

    # Now set up logging according to config
    logger = setup_logging(config)
    logger.debug("Configuration loaded successfully.")

    register = rAppCatalogueClient(args.config)

    if register.register_service():
        logger.info("Service successfully registered on rApp catalogue.")
    else:
        logger.error("Failed to register service.")

    slice_instance = NASPPolicy(config, logger)
    slice_instance.run()
