# rApp-NASP

**Network Aware Slice Policy (NASP) rApp for O-RAN RIC**

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Running Locally](#running-locally)
  - [Docker Setup](#docker-setup)
  - [Kubernetes Deployment with Helm](#kubernetes-deployment-with-helm)
- [API Documentation](#api-documentation)
- [Policy Management Scripts](#policy-management-scripts)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Introduction

**rApp-NASP** is a Policy Management rApp designed for the O-RAN RIC (RAN Intelligent Controller) framework. It facilitates the creation, management, and deployment of network slicing policies, enabling dynamic and efficient control over network resources. This rApp leverages Flask for its API server, integrates with the rApp Catalogue for service registration, and supports containerization and Kubernetes deployment via Helm charts.

## Features

- **Policy Creation API:** Exposes RESTful endpoints to create and manage network slicing policies.
- **Configuration Management:** Uses YAML configuration files for flexible setup.
- **Logging:** Configurable logging levels and formats for monitoring and debugging.
- **Containerization:** Docker support for easy deployment.
- **Kubernetes Support:** Helm charts available for deploying to Kubernetes clusters.
- **Policy Management Scripts:** Shell scripts and JSON schemas for handling policy instances and types.

## Architecture

```
rApp-NASP
├── build_container_image.sh        # Script to build Docker image
├── Dockerfile                      # Dockerfile for containerization
├── helm
│   └── rapp-nasp
│       ├── charts
│       ├── Chart.yaml               # Helm chart configuration
│       ├── templates
│       │   ├── configmap.yaml
│       │   ├── deployment.yaml
│       │   ├── _helpers.tpl
│       │   ├── NOTES.txt
│       │   ├── service.yaml
│       │   └── tests
│       │       └── test-connection.yaml
│       └── values.yaml              # Helm values
├── policy
│   ├── create_policy_instance.bash  # Script to create policy instances
│   ├── create_policy_type.bash      # Script to create policy types
│   ├── delete_policy_type.bash      # Script to delete policy types
│   ├── SliceInstance.json           # JSON schema for policy instances
│   └── SliceSchema.json             # JSON schema for policy types
├── README.md                        # This README
├── requirements.txt                 # Python dependencies
└── src
    ├── config
    │   └── config.yaml               # Configuration file
    ├── __pycache__
    │   └── rApp_catalogue_client.cpython-310.pyc
    ├── rApp_catalogue_client.py      # Client for rApp Catalogue
    └── rApp_NASP.py                  # Main application
```

## Prerequisites

- **Python 3.10+**
- **Docker** (for containerization)
- **Kubernetes Cluster** (optional, for deployment)
- **Helm 3+** (optional, for Kubernetes deployment)
- **rApp Catalogue Access** (for service registration)

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/zanattabruno/rApp-NASP.git
   cd rApp-NASP
   ```

2. **Set Up Virtual Environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

## Configuration

The application uses a YAML configuration file located at `src/config/config.yaml`. Below is an example configuration structure:

```yaml
logging:
  level: INFO

nonrtric:
  ric_id: "ric-12345"
  service_name: "rApp-NASP"
  policytype_id: "policy-type-67890"
  base_url_pms: "https://pms.example.com"  # Policy Management System URL

api_server:
  host: "0.0.0.0"
  port: 5000
```

### Configuration Parameters

- **logging.level:** Sets the logging level (e.g., DEBUG, INFO, WARNING, ERROR).
- **nonrtric.ric_id:** Unique identifier for the RIC instance.
- **nonrtric.service_name:** Name of the rApp service.
- **nonrtric.policytype_id:** Identifier for the policy type managed by this rApp.
- **nonrtric.base_url_pms:** Base URL for the Policy Management System (PMS).
- **api_server.host:** Host address for the API server.
- **api_server.port:** Port number for the API server.

**Note:** Ensure that the `base_url_pms` points to a valid PMS endpoint and that network connectivity is properly configured.

## Usage

### Running Locally

1. **Activate Virtual Environment:**

   ```bash
   source .venv/bin/activate
   ```

2. **Run the Application:**

   ```bash
   python src/rApp_NASP.py --config src/config/config.yaml
   ```

   The API server will start on the configured host and port (default: `0.0.0.0:5000`).

### Docker Setup

1. **Build Docker Image:**

   ```bash
   ./build_container_image.sh
   ```

   *Alternatively, build manually:*

   ```bash
   docker build -t rapp-nasp:latest .
   ```

2. **Run Docker Container:**

   ```bash
   docker run -d -p 5000:5000 --name rapp-nasp rapp-nasp:latest
   ```

   *Ensure that `config.yaml` is appropriately mounted or baked into the Docker image.*

### Kubernetes Deployment with Helm

1. **Navigate to Helm Chart Directory:**

   ```bash
   cd helm/rapp-nasp
   ```

2. **Update `values.yaml` with Configuration:**

   Modify the `values.yaml` file to set configuration parameters as needed.

3. **Deploy with Helm:**

   ```bash
   helm install rapp-nasp ./rapp-nasp
   ```

4. **Verify Deployment:**

   ```bash
   kubectl get pods
   ```

   Ensure that the rApp-NASP pod is running.

## API Documentation

### Create Policy Endpoint

**URL:** `/create_policy`

**Method:** `POST`

**Content-Type:** `application/json`

**Description:** Creates and posts a network slicing policy based on the provided E2 node data.

**Request Body:**

A JSON array of E2 nodes. Each node should include the following fields:

- `mcc` (string): Mobile Country Code.
- `mnc` (string): Mobile Network Code.
- `e2nodeid` (string): Unique identifier for the E2 node.
- `RRMPolicyRatioList` (array, optional): List of RRM policy ratios.

**Example:**

```json
[
  {
    "mcc": "001",
    "mnc": "01",
    "e2nodeid": "node123",
    "RRMPolicyRatioList": [
      {
        "plmnid": "00101",
        "sst": 1,
        "sd": 1,
        "minPRB": 10,
        "maxPRB": 20
      }
    ]
  }
]
```

**Responses:**

- **201 Created**

  ```json
  {
    "status": "success",
    "message": "Policy created successfully."
  }
  ```

- **400 Bad Request**

  ```json
  {
    "status": "failure",
    "message": "Request must be in JSON format."
  }
  ```

  Or

  ```json
  {
    "status": "failure",
    "message": "Invalid data format. Expected a list of E2 nodes."
  }
  ```

- **500 Internal Server Error**

  ```json
  {
    "status": "failure",
    "message": "Failed to create policy."
  }
  ```

## Policy Management Scripts

The `policy` directory contains scripts and JSON schemas for managing policy instances and types.

- **create_policy_instance.bash:** Script to create a policy instance.
- **create_policy_type.bash:** Script to create a policy type.
- **delete_policy_type.bash:** Script to delete a policy type.
- **SliceInstance.json:** JSON schema for policy instances.
- **SliceSchema.json:** JSON schema for policy types.

### Example: Creating a Policy Instance

```bash
./policy/create_policy_instance.bash
```

*Ensure that the PMS endpoint and necessary configurations are correctly set before running the scripts.*

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**

2. **Create a Branch:**

   ```bash
   git checkout -b feature/YourFeature
   ```

3. **Commit Your Changes:**

   ```bash
   git commit -m "Add YourFeature"
   ```

4. **Push to the Branch:**

   ```bash
   git push origin feature/YourFeature
   ```

5. **Open a Pull Request**

Please ensure that your contributions adhere to the project's coding standards and include appropriate tests.

## License

This project is licensed under the [Apache License 2.0](LICENSE).