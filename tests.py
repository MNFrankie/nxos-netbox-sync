

def verify_vlans_exist(netbox_vlans, pyats_vlans): 
    results = {
        "status": False, 
        "PASS": [], 
        "FAIL": [],
    }
    for vlan in netbox_vlans: 
        if str(vlan.vid) in pyats_vlans.keys(): 
            # print(f"✅ {vlan.vid} exists on switch")
            if vlan.name == pyats_vlans[str(vlan.vid)]["name"]: 
                print(f"✅ {vlan.display_name} exists with correct name on switch")
                results["PASS"].append(vlan)
            else: 
                print(f"❌ {vlan.display_name} exists but with WRONG name on switch")
                results["FAIL"].append(vlan)
        else: 
            print(f"❌ {vlan.vid} MISSING from switch")
            results["FAIL"].append(vlan)

    return results

def verify_interface_enabled(netbox_interfaces, pyats_interfaces):
    results = {
        "status": False, 
        "PASS": [], 
        "FAIL": [],
        "VERIFY_DISABLED": []
    }

    for interface in netbox_interfaces: 
        if interface.enabled: 
            interface_status = "Enabled"
        else: 
            interface_status = "Disabled"

        # NOTE: Current bug in Genie model reports an interface as "enabled": False even if 
        #       the interface is "no shut". Reported to team.. will need to skip tests for 
        #       interfaces that are Enabled on the device, when they should be disabled.
        if interface.name in pyats_interfaces.keys(): 
            # print(f"✅ {interface.name} found on switch")
            if interface.enabled:
                if pyats_interfaces[interface.name]["enabled"]:
                    # Test 1: NB Enabled - pyATS enabled and oper_status up
                    if pyats_interfaces[interface.name]["oper_status"] == "up": 
                        print(f"✅ {interface.name} was correctly found to be UP/UP on switch")
                        results["PASS"].append(interface)
                    # Test 2: NB Enabled - pyATS enabled and oper_status down
                    elif pyats_interfaces[interface.name]["oper_status"] == "down": 
                        print(f"❌ {interface.name} was incorrectly found to be UP/DOWN on switch")
                        results["PASS"].append(interface)
                # Test 3: NB Enabled - pyATS disabled
                elif not pyats_interfaces[interface.name]["enabled"]:
                    print(f"❌ {interface.name} was incorrectly found to be DOWN/DOWN on switch")
                    results["PASS"].append(interface)
            # See note above.. skipping these tests for now as they are inaccurate
            elif not interface.enabled: 
                if pyats_interfaces[interface.name]["enabled"]:
                    # Test 4: NB DISABLED - pyATS enabled and oper_status up
                    if pyats_interfaces[interface.name]["oper_status"] == "up": 
                        print(f"❌ {interface.name} was incorrectly found to be UP/UP on switch")
                        results["FAIL"].append(interface)
                    # See note above.. skipping these tests for now as they are inaccurate
                    # Test 5: NB DISABLED - pyATS enabled and oper_status down
                    # elif pyats_interfaces[interface.name]["oper_status"] == "down": 
                    #     print(f"❌ {interface.name} was incorrectly found to be UP/DOWN on switch")
                # See note above.. skipping these tests for now as they are inaccurate
                # Test 6: NB DISABLED - pyATS disabled
                # elif not pyats_interfaces[interface.name]["enabled"]:
                #     print(f"✅ {interface.name} was correctly found to be DOWN/DOWN on switch")
                results["VERIFY_DISABLED"].append(interface)

        else: 
            print(f"❌ {interface.name} MISSING from switch")
            results["FAIL"].append(interface)

    return results