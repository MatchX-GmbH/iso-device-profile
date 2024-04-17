# ===========================================================================
# Python3 script
# ===========================================================================
import os
import sys
import getopt
import zlib
import array
import json 
import zipfile

# ===========================================================================
# Global variables
# ===========================================================================
gVerbose = False

# ===========================================================================
# ===========================================================================
def showUsage():
    print("Usage: " + sys.argv[0] + " [OPTIONS]")
    print("      -h, --help                 Show this help.")
    print("      -v, --verbose              Verbose output.")
    print(" ")


def getCommandLineArg():
    global gVerbose
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hc:v", [
            "help", "config="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(str(err))  # will print something like "option -a not recognized"
        showUsage()
        return False

    for o, a in opts:
        if o == "-v":
            gVerbose = True
        elif o in ("-h", "--help"):
            showUsage()
            sys.exit()
        else:
            print ("unhandled option")
            return False       

    return True

# ===========================================================================
# Read/Write JSON file
# ===========================================================================
def readJsonFile(aFilePath):
    if not os.path.exists(aFilePath):
        print(f"ERROR: {aFilePath} not found.")
        return {}

    with open(aFilePath) as f:
        d = json.load(f)
        return d
    
def writeJsonFile(aFilePath, aObject):
    with open(aFilePath, "w") as f:
        f.write(json.dumps(aObject, indent=2))

# ===========================================================================
# Check Device Profile JSON
# ===========================================================================
def checkDeviceProfileJson(aObject, aPath):
    if not "name" in aObject:
        print (f"ERROR: 'name' not found.")
        return False
    if not "region" in aObject:
        print (f"ERROR: 'region' not found.")
        return False
    if not "macVersion" in aObject:
        print (f"ERROR: 'macVersion' not found.")
        return False
    if not "regParamRevision" in aObject:
        print (f"ERROR: 'regParamRevision' not found.")
        return False
    if not "adrAlgorithmId" in aObject:
        print (f"ERROR: 'adrAlgorithmId' not found.")
        return False
    if not "expectedUpInterval" in aObject:
        print (f"ERROR: 'expectedUpInterval' not found.")
        return False
    if not "deviceStatusReqPerDay" in aObject:
        print (f"ERROR: 'deviceStatusReqPerDay' not found.")
        return False
    if not "codecUrl" in aObject:
        print (f"ERROR: 'codecUrl' not found.")
        return False
    if not "classC" in aObject:
        print (f"ERROR: 'classC' not found.")
        return False
    if not "image" in aObject:
        print (f"ERROR: 'image' not found.")
        return False
    
    # Check region
    obj_region = aObject["region"]
    supported_region = ["EU868", "US915", "CN470", "KR920", "AU915", "AS923", "ISM2400"]
    if not obj_region in supported_region:
        print (f"ERROR: region '{obj_region}' not supported.")
        return False
    
    # Check macVersion
    obj_macVersion = aObject["macVersion"]
    supported_macVersion = ["1.0.0", "1.0.1",  "1.0.2",  "1.0.3", "1.0.4", "1.1.0"]
    if not obj_macVersion in supported_macVersion:
        print (f"ERROR: macVersion '{obj_macVersion}' not supported.")
        return False

    # Check regParamRevision
    obj_regParamRevision = aObject["regParamRevision"]
    supported_regParamRevision = ["A", "B", "RP002-1.0.0", "RP002-1.0.1", "RP002-1.0.2", "RP002-1.0.3"]
    if not obj_regParamRevision in supported_regParamRevision:
        print (f"ERROR: regParamRevision '{obj_regParamRevision}' not supported.")
        return False

    # Check adrAlgorithmId
    obj_adrAlgorithmId = aObject["adrAlgorithmId"]
    supported_adrAlgorithmId = ["default", "lora_lr_fhss" or "lr_fhss"]
    if not obj_adrAlgorithmId in supported_adrAlgorithmId:
        print (f"ERROR: adrAlgorithmId '{obj_adrAlgorithmId}' not supported.")
        return False
    
    # Check codecUrl
    obj_codecUrl = aObject["codecUrl"]
    codec_filepath = os.path.join(os.path.dirname(aPath), obj_codecUrl)
    if not os.path.exists(codec_filepath):
        print(f"ERROR: {obj_codecUrl} not found.")
        return False
    
    # Check image
    obj_image = aObject["image"]
    image_filepath = os.path.join(os.path.dirname(aPath), obj_image)
    if not os.path.exists(image_filepath):
        print(f"ERROR: {obj_image} not found.")
        return False
    file_part = os.path.splitext(image_filepath)
    if file_part[1].lower() != ".jpeg":
        print(f"ERROR: {obj_image} invalid file extension.")
        return False

    return True


# ===========================================================================
# Check Sensor Types JSON
# ===========================================================================
def checkSensorTypesJson(aObject, aPath):
    if not "name" in aObject:
        print (f"ERROR: 'name' not found.")
        return False
    
    return True

# ===========================================================================
# Main
# ===========================================================================

def main():
    if (getCommandLineArg() == False):
        sys.exit(1)

    output_list = []

    # Check syntax of sensor_type.json
    target_filepath = "sensor_types.json"
    print (f"Checking {target_filepath}")
    j_sensor_type = readJsonFile(target_filepath)
    if not isinstance(j_sensor_type, list):
        print (f"{target_filepath}: Invalid  JSON. Top level is not a list.")
        sys.exit(1)
    for item in j_sensor_type:
        if not checkSensorTypesJson(item, target_filepath):
            print (f"Check {target_filepath} failed.")
            sys.exit(1)
    print (f"  {target_filepath} is good.")

    # scan all directory
    with os.scandir() as top_dir_list:
        for company in top_dir_list:
            sensor_list = []

            if not company.is_dir():
                continue
            
            # Filter out unwanted name
            if company.name == ".git":
                continue

            # Read info.json to get the full name
            j_info = readJsonFile(os.path.join(company.path, "info.json"))
            if not "name" in j_info:
                print(f"ERROR. 'name' not found for directory '{company.name}'. Skipped.")
                continue
            company_full_name=j_info["name"]

            #
            print (f"Processing '{company.path}' ({company_full_name})...")
            with os.scandir(company.path) as company_dir_list:
                for json_file in company_dir_list:
                    if not json_file.is_file():
                        continue

                    # Filter out unwanted file name
                    file_part = os.path.splitext(json_file.name)
                    if file_part[0] == "info" or file_part[1] != ".json":
                        continue
                    
                    # Check Sensor JSON file
                    if json_file.stat().st_size > (128 * 1024):
                        raise Exception(f"File too large. '{json_file.path}'")

                    j_sensor = readJsonFile(json_file.path)
                    if not checkDeviceProfileJson(j_sensor, json_file.path):
                        raise Exception(f"Invalid Device Profile JSON file. '{json_file.path}'")
                    
                    # Add to list
                    sensor_name = j_sensor["name"]
                    sensor_path = os.path.join(".", company.name, json_file.name)
                    print(f"  {json_file.name} is OK. '{sensor_name}' added.")
                    sensor_info = {"name": sensor_name, "path":sensor_path}
                    sensor_list.insert(len(sensor_list), sensor_info)

            if len(sensor_list) == 0:
                print ("  No item. Skipped.")
                continue
            
            sensor_list.sort(key=lambda x: x["name"])
            output_list.insert(len(output_list), {"name":company_full_name, "deviceProfileList":sensor_list})
            print (f"  Total {len(sensor_list)} item(s) found.")
    
    output_list.sort(key=lambda x: x["name"])
    output_filepath = "list.json"
    writeJsonFile(output_filepath, output_list)
    print (f"Saved to '{output_filepath}'.")

# ===========================================================================
# ===========================================================================
if __name__ == "__main__":
    main()