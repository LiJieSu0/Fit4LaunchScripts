import React from 'react';
import './table-styles.css'; // Assuming a shared CSS for tables

const coverageData = {
    "5G VoNR Coverage Test": {
        "DUT1_Run1": {
            "last_mos_value_coords": {
                "latitude": "47.146212",
                "longitude": "-122.357310",
                "distance_to_base_station_km": 1.999446329912468
            },
            "voice_call_drop_coords": {
                "latitude": "47.147595",
                "longitude": "-122.357257",
                "distance_to_base_station_km": 2.153132266606282
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.144150",
                "longitude": "-122.357327",
                "distance_to_base_station_km": 1.7702410668954354
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.144150",
                "longitude": "-122.357327",
                "distance_to_base_station_km": 1.7702410668954354
            }
        },
        "DUT1_Run2": {
            "last_mos_value_coords": {
                "latitude": "47.148943",
                "longitude": "-122.357210",
                "distance_to_base_station_km": 2.3029527740450657
            },
            "voice_call_drop_coords": {
                "latitude": "47.149857",
                "longitude": "-122.357205",
                "distance_to_base_station_km": 2.4045708172663485
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.145997",
                "longitude": "-122.357313",
                "distance_to_base_station_km": 1.975548582054853
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.145685",
                "longitude": "-122.357318",
                "distance_to_base_station_km": 1.9408705100062769
            }
        },
        "DUT1_Run3": {
            "last_mos_value_coords": {
                "latitude": "47.149588",
                "longitude": "-122.357208",
                "distance_to_base_station_km": 2.374664934842879
            },
            "voice_call_drop_coords": {
                "latitude": "47.149990",
                "longitude": "-122.357202",
                "distance_to_base_station_km": 2.4193555824386777
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.147635",
                "longitude": "-122.357265",
                "distance_to_base_station_km": 2.1575894203109978
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.147347",
                "longitude": "-122.357282",
                "distance_to_base_station_km": 2.1255917846670713
            }
        },
        "DUT1_Run4": {
            "last_mos_value_coords": {
                "latitude": "47.150210",
                "longitude": "-122.357212",
                "distance_to_base_station_km": 2.4438261909730916
            },
            "voice_call_drop_coords": {
                "latitude": "47.150355",
                "longitude": "-122.357207",
                "distance_to_base_station_km": 2.4599432466653592
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.146830",
                "longitude": "-122.357288",
                "distance_to_base_station_km": 2.068121176668293
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.146405",
                "longitude": "-122.357303",
                "distance_to_base_station_km": 2.020892676021095
            }
        },
        "DUT1_Run5": {
            "last_mos_value_coords": {
                "latitude": "47.147903",
                "longitude": "-122.357212",
                "distance_to_base_station_km": 2.187323721431919
            },
            "voice_call_drop_coords": {
                "latitude": "47.149065",
                "longitude": "-122.357143",
                "distance_to_base_station_km": 2.316453659937113
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.146368",
                "longitude": "-122.357287",
                "distance_to_base_station_km": 2.0167563867746545
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.146200",
                "longitude": "-122.357295",
                "distance_to_base_station_km": 1.998090320737716
            }
        },
        "DUT2_Run1": {
            "last_mos_value_coords": {
                "latitude": "47.153447",
                "longitude": "-122.357128",
                "distance_to_base_station_km": 2.8036728639963595
            },
            "voice_call_drop_coords": {
                "latitude": "47.153982",
                "longitude": "-122.357142",
                "distance_to_base_station_km": 2.863169349784437
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.150115",
                "longitude": "-122.357223",
                "distance_to_base_station_km": 2.433274574224882
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.149238",
                "longitude": "-122.357208",
                "distance_to_base_station_km": 2.335750185459279
            }
        },
        "DUT2_Run2": {
            "last_mos_value_coords": {
                "latitude": "47.153057",
                "longitude": "-122.357150",
                "distance_to_base_station_km": 2.7603244741222004
            },
            "voice_call_drop_coords": {
                "latitude": "47.153587",
                "longitude": "-122.357118",
                "distance_to_base_station_km": 2.819232801029553
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.150577",
                "longitude": "-122.357187",
                "distance_to_base_station_km": 2.484607879294723
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.149915",
                "longitude": "-122.357213",
                "distance_to_base_station_km": 2.4110274957975864
            }
        },
        "DUT2_Run3": {
            "last_mos_value_coords": {
                "latitude": "47.150025",
                "longitude": "-122.357193",
                "distance_to_base_station_km": 2.4232384695270377
            },
            "voice_call_drop_coords": {
                "latitude": "47.150025",
                "longitude": "-122.357193",
                "distance_to_base_station_km": 2.4232384695270377
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.150508",
                "longitude": "-122.357250",
                "distance_to_base_station_km": 2.476998045001702
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.150508",
                "longitude": "-122.357250",
                "distance_to_base_station_km": 2.476998045001702
            }
        },
        "DUT2_Run4": {
            "last_mos_value_coords": {
                "latitude": "47.153377",
                "longitude": "-122.357125",
                "distance_to_base_station_km": 2.7958874866968526
            },
            "voice_call_drop_coords": {
                "latitude": "47.153743",
                "longitude": "-122.357128",
                "distance_to_base_station_km": 2.836585225200065
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.150520",
                "longitude": "-122.357190",
                "distance_to_base_station_km": 2.4782729739519347
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.150442",
                "longitude": "-122.357187",
                "distance_to_base_station_km": 2.4695976565480917
            }
        },
        "DUT2_Run5": {
            "last_mos_value_coords": {
                "latitude": "47.150565",
                "longitude": "-122.357137",
                "distance_to_base_station_km": 2.483231016514379
            },
            "voice_call_drop_coords": {
                "latitude": "47.150565",
                "longitude": "-122.357137",
                "distance_to_base_station_km": 2.483231016514379
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.148665",
                "longitude": "-122.357153",
                "distance_to_base_station_km": 2.2719876333984743
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.147835",
                "longitude": "-122.357215",
                "distance_to_base_station_km": 2.1797665859267155
            }
        },
        "DUT3_Run1": {
            "last_mos_value_coords": {
                "latitude": "47.149363",
                "longitude": "-122.357208",
                "distance_to_base_station_km": 2.349648297025474
            },
            "voice_call_drop_coords": {
                "latitude": "47.150112",
                "longitude": "-122.357222",
                "distance_to_base_station_km": 2.4329400070981344
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.147123",
                "longitude": "-122.357272",
                "distance_to_base_station_km": 2.10067474492016
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.146212",
                "longitude": "-122.357310",
                "distance_to_base_station_km": 1.999446329912468
            }
        },
        "DUT3_Run2": {
            "last_mos_value_coords": {
                "latitude": "47.148943",
                "longitude": "-122.357210",
                "distance_to_base_station_km": 2.3029527740450657
            },
            "voice_call_drop_coords": {
                "latitude": "47.149857",
                "longitude": "-122.357205",
                "distance_to_base_station_km": 2.4045708172663485
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.145837",
                "longitude": "-122.357317",
                "distance_to_base_station_km": 1.9577670810020824
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.144660",
                "longitude": "-122.357317",
                "distance_to_base_station_km": 1.8269195169048589
            }
        },
        "DUT3_Run3": {
            "last_mos_value_coords": {
                "latitude": "47.149588",
                "longitude": "-122.357208",
                "distance_to_base_station_km": 2.374664934842879
            },
            "voice_call_drop_coords": {
                "latitude": "47.149973",
                "longitude": "-122.357202",
                "distance_to_base_station_km": 2.4174654241661178
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.144538",
                "longitude": "-122.357355",
                "distance_to_base_station_km": 1.8134221897612766
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.144193",
                "longitude": "-122.357358",
                "distance_to_base_station_km": 1.775076210196034
            }
        },
        "DUT3_Run4": {
            "last_mos_value_coords": {
                "latitude": "47.150210",
                "longitude": "-122.357212",
                "distance_to_base_station_km": 2.4438261909730916
            },
            "voice_call_drop_coords": {
                "latitude": "47.150357",
                "longitude": "-122.357203",
                "distance_to_base_station_km": 2.460161776803299
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.144723",
                "longitude": "-122.357368",
                "distance_to_base_station_km": 1.8340107367357248
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.144028",
                "longitude": "-122.357372",
                "distance_to_base_station_km": 1.7567605690275414
            }
        },
        "DUT3_Run5": {
            "last_mos_value_coords": {
                "latitude": "47.149548",
                "longitude": "-122.357143",
                "distance_to_base_station_km": 2.370157360637832
            },
            "voice_call_drop_coords": {
                "latitude": "47.149815",
                "longitude": "-122.357147",
                "distance_to_base_station_km": 2.3998479318470487
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.144938",
                "longitude": "-122.357303",
                "distance_to_base_station_km": 1.8578021880856386
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.143677",
                "longitude": "-122.357317",
                "distance_to_base_station_km": 1.7176423814983304
            }
        },
        "REF1_Run1": {
            "last_mos_value_coords": {
                "latitude": "47.150115",
                "longitude": "-122.357223",
                "distance_to_base_station_km": 2.433274574224882
            },
            "voice_call_drop_coords": {
                "latitude": "47.150115",
                "longitude": "-122.357223",
                "distance_to_base_station_km": 2.433274574224882
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.148357",
                "longitude": "-122.357232",
                "distance_to_base_station_km": 2.2378229982269593
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.143685",
                "longitude": "-122.357327",
                "distance_to_base_station_km": 1.718549348813673
            }
        },
        "REF1_Run2": {
            "last_mos_value_coords": {
                "latitude": "47.149915",
                "longitude": "-122.357213",
                "distance_to_base_station_km": 2.4110274957975864
            },
            "voice_call_drop_coords": {
                "latitude": "47.149915",
                "longitude": "-122.357213",
                "distance_to_base_station_km": 2.4110274957975864
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.148252",
                "longitude": "-122.357233",
                "distance_to_base_station_km": 2.226149961502694
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.145408",
                "longitude": "-122.357322",
                "distance_to_base_station_km": 1.9100824205127644
            }
        },
        "REF1_Run3": {
            "last_mos_value_coords": {
                "latitude": "47.150025",
                "longitude": "-122.357193",
                "distance_to_base_station_km": 2.4232384695270377
            },
            "voice_call_drop_coords": {
                "latitude": "47.150025",
                "longitude": "-122.357193",
                "distance_to_base_station_km": 2.4232384695270377
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.148292",
                "longitude": "-122.357238",
                "distance_to_base_station_km": 2.2306029475933355
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.144018",
                "longitude": "-122.357358",
                "distance_to_base_station_km": 1.7556228232091218
            }
        },
        "REF1_Run4": {
            "last_mos_value_coords": {
                "latitude": "47.150355",
                "longitude": "-122.357202",
                "distance_to_base_station_km": 2.459938450039336
            },
            "voice_call_drop_coords": {
                "latitude": "47.150355",
                "longitude": "-122.357202",
                "distance_to_base_station_km": 2.459938450039336
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.148438",
                "longitude": "-122.357220",
                "distance_to_base_station_km": 2.2468155335562643
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.145000",
                "longitude": "-122.357350",
                "distance_to_base_station_km": 1.8647718658639865
            }
        },
        "REF1_Run5": {
            "last_mos_value_coords": {
                "latitude": "47.148500",
                "longitude": "-122.357162",
                "distance_to_base_station_km": 2.253650157626519
            },
            "voice_call_drop_coords": {
                "latitude": "47.150073",
                "longitude": "-122.357145",
                "distance_to_base_station_km": 2.428532779798981
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.147258",
                "longitude": "-122.357242",
                "distance_to_base_station_km": 2.1156461087844294
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.143857",
                "longitude": "-122.357312",
                "distance_to_base_station_km": 1.7376435760086983
            }
        },
        "REF2_Run1": {
            "last_mos_value_coords": {
                "latitude": "47.150115",
                "longitude": "-122.357223",
                "distance_to_base_station_km": 2.433274574224882
            },
            "voice_call_drop_coords": {
                "latitude": "47.150115",
                "longitude": "-122.357223",
                "distance_to_base_station_km": 2.433274574224882
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.148512",
                "longitude": "-122.357228",
                "distance_to_base_station_km": 2.255051874733711
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.143820",
                "longitude": "-122.357325",
                "distance_to_base_station_km": 1.733553011301319
            }
        },
        "REF2_Run2": {
            "last_mos_value_coords": {
                "latitude": "47.149915",
                "longitude": "-122.357213",
                "distance_to_base_station_km": 2.4110274957975864
            },
            "voice_call_drop_coords": {
                "latitude": "47.149915",
                "longitude": "-122.357213",
                "distance_to_base_station_km": 2.4110274957975864
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.149627",
                "longitude": "-122.357207",
                "distance_to_base_station_km": 2.3790001576221136
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.148822",
                "longitude": "-122.357212",
                "distance_to_base_station_km": 2.2895015579028613
            }
        },
        "REF2_Run3": {
            "last_mos_value_coords": {
                "latitude": "47.150027",
                "longitude": "-122.357197",
                "distance_to_base_station_km": 2.423464647333355
            },
            "voice_call_drop_coords": {
                "latitude": "47.150025",
                "longitude": "-122.357193",
                "distance_to_base_station_km": 2.4232384695270377
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.149655",
                "longitude": "-122.357207",
                "distance_to_base_station_km": 2.3821133447872787
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.148478",
                "longitude": "-122.357230",
                "distance_to_base_station_km": 2.2512738734415643
            }
        },
        "REF2_Run4": {
            "last_mos_value_coords": {
                "latitude": "47.150355",
                "longitude": "-122.357202",
                "distance_to_base_station_km": 2.459938450039336
            },
            "voice_call_drop_coords": {
                "latitude": "47.150355",
                "longitude": "-122.357202",
                "distance_to_base_station_km": 2.459938450039336
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.149763",
                "longitude": "-122.357213",
                "distance_to_base_station_km": 2.3941273521300293
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.146830",
                "longitude": "-122.357288",
                "distance_to_base_station_km": 2.068121176668293
            }
        },
        "REF2_Run5": {
            "last_mos_value_coords": {
                "latitude": "47.150565",
                "longitude": "-122.357137",
                "distance_to_base_station_km": 2.483231016514379
            },
            "voice_call_drop_coords": {
                "latitude": "47.150565",
                "longitude": "-122.357137",
                "distance_to_base_station_km": 2.483231016514379
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.148427",
                "longitude": "-122.357165",
                "distance_to_base_station_km": 2.2455363958909924
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.148018",
                "longitude": "-122.357203",
                "distance_to_base_station_km": 2.2001000723350073
            }
        },
        "REF3_Run1": {
            "last_mos_value_coords": {
                "latitude": "47.149363",
                "longitude": "-122.357208",
                "distance_to_base_station_km": 2.349648297025474
            },
            "voice_call_drop_coords": {
                "latitude": "47.150115",
                "longitude": "-122.357223",
                "distance_to_base_station_km": 2.433274574224882
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.144788",
                "longitude": "-122.357325",
                "distance_to_base_station_km": 1.8411622808694674
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.143685",
                "longitude": "-122.357327",
                "distance_to_base_station_km": 1.718549348813673
            }
        },
        "REF3_Run2": {
            "last_mos_value_coords": {
                "latitude": "47.148943",
                "longitude": "-122.357210",
                "distance_to_base_station_km": 2.3029527740450657
            },
            "voice_call_drop_coords": {
                "latitude": "47.149928",
                "longitude": "-122.357207",
                "distance_to_base_station_km": 2.412466956271034
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.145997",
                "longitude": "-122.357313",
                "distance_to_base_station_km": 1.975548582054853
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.144793",
                "longitude": "-122.357317",
                "distance_to_base_station_km": 1.8417049749082302
            }
        },
        "REF3_Run3": {
            "last_mos_value_coords": {
                "latitude": "47.149588",
                "longitude": "-122.357208",
                "distance_to_base_station_km": 2.374664934842879
            },
            "voice_call_drop_coords": {
                "latitude": "47.150010",
                "longitude": "-122.357203",
                "distance_to_base_station_km": 2.421580268166885
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.144712",
                "longitude": "-122.357352",
                "distance_to_base_station_km": 1.8327595672380992
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.142960",
                "longitude": "-122.357353",
                "distance_to_base_station_km": 1.6380062585025181
            }
        },
        "REF3_Run4": {
            "last_mos_value_coords": {
                "latitude": "47.150210",
                "longitude": "-122.357212",
                "distance_to_base_station_km": 2.4438261909730916
            },
            "voice_call_drop_coords": {
                "latitude": "47.150357",
                "longitude": "-122.357205",
                "distance_to_base_station_km": 2.4601636929551476
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.143407",
                "longitude": "-122.357368",
                "distance_to_base_station_km": 1.6877231050805068
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.143092",
                "longitude": "-122.357368",
                "distance_to_base_station_km": 1.6527086275241574
            }
        },
        "REF3_Run5": {
            "last_mos_value_coords": {
                "latitude": "47.148500",
                "longitude": "-122.357162",
                "distance_to_base_station_km": 2.253650157626519
            },
            "voice_call_drop_coords": {
                "latitude": "47.150515",
                "longitude": "-122.357142",
                "distance_to_base_station_km": 2.4776755898390825
            },
            "first_dl_tp_gt_1_coords": {
                "latitude": "47.143677",
                "longitude": "-122.357317",
                "distance_to_base_station_km": 1.7176423814983304
            },
            "first_ul_tp_gt_1_coords": {
                "latitude": "47.142942",
                "longitude": "-122.357317",
                "distance_to_base_station_km": 1.6359370544577592
            }
        }
    }
};

const processData = (metricKey) => {
    const devices = ["DUT1", "DUT2", "DUT3", "REF1", "REF2", "REF3"];
    const runs = ["Run1", "Run2", "Run3", "Run4", "Run5"];
    const tableData = {};

    devices.forEach(device => {
        tableData[device] = {};
        let sumDistance = 0;
        let runCount = 0;

        runs.forEach(run => {
            const key = `${device}_${run}`;
            if (coverageData["5G VoNR Coverage Test"][key] && coverageData["5G VoNR Coverage Test"][key][metricKey]) {
                const distance = parseFloat(coverageData["5G VoNR Coverage Test"][key][metricKey].distance_to_base_station_km);
                tableData[device][run] = distance.toFixed(3);
                sumDistance += distance;
                runCount++;
            } else {
                tableData[device][run] = 'N/A';
            }
        });

        tableData[device].Average = runCount > 0 ? (sumDistance / runCount).toFixed(3) : 'N/A';
    });
    return tableData;
};

const renderTable = (title, data) => {
    const runs = ["Run1", "Run2", "Run3", "Run4", "Run5"];
    const deviceNames = Object.keys(data);

    return (
        <div className="table-container">
            <h3>{title}</h3>
            <table className="common-table">
                <thead>
                    <tr>
                        <th>Device Name</th>
                        {runs.map(run => <th key={run}>{run}</th>)}
                        <th>Average</th>
                    </tr>
                </thead>
                <tbody>
                    {deviceNames.map(device => (
                        <tr key={device}>
                            <td>{device}</td>
                            {runs.map(run => (
                                <td key={`${device}-${run}`}>{data[device][run]}</td>
                            ))}
                            <td>{data[device].Average}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
};

const CoverageTables = () => {
    const lastMosData = processData("last_mos_value_coords");
    const voiceCallDropData = processData("voice_call_drop_coords");
    const dlTpData = processData("first_dl_tp_gt_1_coords");
    const ulTpData = processData("first_ul_tp_gt_1_coords");

    return (
        <div>
            {renderTable("Last MOS Value Distance (km)", lastMosData)}
            {renderTable("Voice Call Drop Distance (km)", voiceCallDropData)}
            {renderTable("DL TP < 1 Distance (km)", dlTpData)}
            {renderTable("UL TP < 1 Distance (km)", ulTpData)}
        </div>
    );
};

export default CoverageTables;
