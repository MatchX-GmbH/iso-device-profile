# Device Profile for ISO Devices

## Introduction

These are the device profile for the ISO devices.



## How to Submit Your Device Profile

1. **Fork this repository**: Click on the 'Fork' button at the top right of this page and create a copy of this repository in your own GitHub account.

2. **Clone your forked repository**: Navigate to your GitHub account, open the forked repository, and click the 'Code' button. Then copy the URL and clone the repository to your local system.

3. **Create a new Device Profile for your ISO device**: Create the Device Profile JSON file under a directory as your company name. For individual developer, place the file under `individual` directory. Also place a javascript codec file and a image file (JPEG).

4. Run the `gen_list.py` to update the `list.json`. It will check the content of the new added JSON file.

   ```
   python gen_list.py
   ```

5. **Commit and push your changes**: Once you've added your Device Profile JSON and related files, commit and push the changes to your forked repository.

6. **Create a pull request**: Go back to your forked repository on GitHub and click on 'New pull request'. In the pull request comment, provide any additional information about your Device Profile.

Your pull request will be reviewed and, if everything is in order, your Device Profile will be available in the ISO DApp for select.



## Device Profile JSON file

Maximum size 128KiB.

```
{
  "name": "...",
  "region": "...",
  "macVersion": "...",
  "regParamRevision": "...",
  "adrAlgorithm": "...",
  "expectedUpInterval": #,
  "deviceStatusReqPerDay": #,
  "codecUrl": "...",
  "classC": false
}
```

| Item                  | Description                                                  |
| --------------------- | ------------------------------------------------------------ |
| name                  | The name of the profile.                                     |
| region                | The region of the device.<br />Supported values: "EU868", "US915", "CN470", "KR920", "AU915", "AS923" |
| macVersion            | The LoRaWAN MAC version supported by the device.<br />Possible values: "1.0.0", "1.0.1",  "1.0.2",  "1.0.3", "1.0.4", "1.1.0" |
| regParamRevision      | Revision of the Regional Parameters specification supported by the device.<br />Possible values: "A", "B", "RP002-1.0.0", "RP002-1.0.1", "RP002-1.0.2", "RP002-1.0.3" |
| adrAlgorithmId        | The ADR algorithm that will be used for controlling the device data-rate.<br />Possible values: "default", "lora_lr_fhss" or "lr_fhss". |
| expectedUpInterval    | The expected interval in seconds in which the device sends uplink messages. |
| deviceStatusReqPerDay | Frequency to initiate an End-Device status request (request/day). Set to 0 to disable. |
| codecUrl              | The URL for the codec js file.                               |
| classC                | Supports Class-C.                                            |
| image                 | The image file.                                              |



The Codec js file contains 2 entry functions, `decodeUplink(input) {}` and `encodeDownlink(input) {}`. The ChirpVM will call `decodeUplink` when a Uplink happens, and call `encodeDownlink` before queuing a Downlink.

[Example JSON file](./matchx/x2e_env_sensor_eu868.json)

[Example Codec js file](./matchx/matchx_generic_codec.js)
