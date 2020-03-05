# tap-outreach

This is a [Singer](https://singer.io) tap that produces JSON-formatted data
following the [Singer
spec](https://github.com/singer-io/getting-started/blob/master/SPEC.md).

This tap:

- Pulls raw data from https://api.outreach.io/api/ 
- Extracts the following resources:
  - calls, email address, mailboxes, mailings, profiles, prospects, roles, sequences, sequence states, sequence steps, sequence templates, stages, tasks, teams, and users
- Outputs the schema for each resource
- Incrementally pulls data based on the input state

---
## Streams

[Calls](https://api.outreach.io/api/v2/docs#call)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt  
- Connections
  - Provides Data Connections to outside systems such as salesforce
  
[Email Address](https://api.outreach.io/api/v2/docs#emailAddress)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt  

[Mailboxes](https://api.outreach.io/api/v2/docs#mailbox)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt  

[Mailings](https://api.outreach.io/api/v2/docs#mailing)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt  
- Connections
  - Provides Data Connections to outside systems such as salesforce

[Profiles](https://api.outreach.io/api/v2/docs#profile)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt 

[Prospects](https://api.outreach.io/api/v2/docs#prospect)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt  
- Connections
  - Provides Data Connections to outside systems such as salesforce

[Roles](https://api.outreach.io/api/v2/docs#role)
- Primary key fields: id
- Replication strategy: FULL 
  - Key: none  

[Sequences](https://api.outreach.io/api/v2/docs#sequence)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt  

[Sequence States](https://api.outreach.io/api/v2/docs#sequenceState)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt  

[Sequence Steps](https://api.outreach.io/api/v2/docs#sequenceStep)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt  

[Sequence Templates](https://api.outreach.io/api/v2/docs#sequenceTemplate)
- Primary key fields: id
- Replication strategy: FULL 
  - Key: updatedAt  

[Stages](https://api.outreach.io/api/v2/docs#stage)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt  
- Connections
  - Provides Data Connections to outside systems such as salesforce

[Tasks](https://api.outreach.io/api/v2/docs#task)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt  
- Connections
  - Provides Data Connections to outside systems such as salesforce

[Teams](https://api.outreach.io/api/v2/docs#team)
- Primary key fields: id
- Replication strategy: FULL 
  - Key: none  

[Users](https://api.outreach.io/api/v2/docs#user)
- Primary key fields: id
- Replication strategy: INCREMENTAL 
  - Key: updatedAt  
- Connections
  - Provides Data Connections to outside systems such as salesforce

## Quick Start

1. Install

    Clone this repository, and then install using pip. We recommend using a virtualenv:

    ```
    > cd .../tap-kustomer
    > pip install .
    ```
   
2. Dependent libraries
    The following dependent libraries were installed.
    ```
    > pip install singer-python
    > pip install jsonschema
    > pip install requests
    ```
 
 3. Create your tap's `config.json` file. The `refresh_token`, `client_id`, and `client_secret` are the credentials you generate through outreach.  Information can be found [here](https://api.outreach.io/api/v2/docs#authentication)
 
     ```json
    {
        "refresh_token": "YOUR_REFERESH_TOKEN",
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "start_date": "2020-02-06T00:00:00Z",
        "end_date": "2020-02-07T00:00:00Z"
    } 
    
4. Run the Tap in Discovery Mode
    This creates a catalog.json for selecting objects/fields to integrate:
    ```bash
    tap-outreach --config config.json --discover > catalog.json
    ```
   See the Singer docs on discovery mode
   [here](https://github.com/singer-io/getting-started/blob/master/docs/DISCOVERY_MODE.md#discovery-mode).
   
5. Run the Tap in Sync Mode (with catalog) and [write out to state file](https://github.com/singer-io/getting-started/blob/master/docs/RUNNING_AND_DEVELOPING.md#running-a-singer-tap-with-a-singer-target)

    For Sync mode:
    ```bash
    > tap-outreach --config tap_config.json --catalog catalog.json > state.json
    ```
    
6. Test the Tap
    
    While developing the outreach tap, the following utilities were leveraged in accordance with Singer.io best practices:
    Pylint to improve [code quality](https://github.com/singer-io/getting-started/blob/master/docs/BEST_PRACTICES.md#code-quality):
    ```bash
    > pylint tap_outreach -d missing-docstring -d logging-format-interpolation -d too-many-locals -d too-many-arguments
    ```
    Pylint test resulted in the following score:
    ```bash
    Your code has been rated at 9.62/10
   ```
    Validating no errors:
   ```bash
    > pylint --errors-only tap_outreach
    ```
    Pylint test resulted in the following score:
    ```bash
    
   ```
    To [check the tap](https://github.com/singer-io/singer-tools#singer-check-tap) and verify working:
    ```bash
    > tap-outreach --config tap_config.json  | singer-check-tap > state.json
    ```
    Check tap resulted in the following:
    ```bash
    The output is valid.
    It contained 32133 messages for 13 streams.
    
         13 schema messages
      32107 record messages
         13 state messages
    
    Details by stream:
    +----------------+---------+---------+
    | stream         | records | schemas |
    +----------------+---------+---------+
    | stages         | 0       | 1       |
    | users          | 3       | 1       |
    | roles          | 245     | 1       |
    | teams          | 40      | 1       |
    | sequences      | 28      | 1       |
    | sequencestates | 5210    | 1       |
    | sequencesteps  | 195     | 1       |
    | mailings       | 11000   | 1       |
    | mailboxes      | 1       | 1       |
    | prospects      | 8731    | 1       |
    | profiles       | 13      | 1       |
    | calls          | 1370    | 1       |
    | tasks          | 5271    | 1       |
    +----------------+---------+---------+

    ```
---


Copyright &copy; 2018 Stitch
