# Team - MASTER DATA MINDS
# This script is a Streamlit application that generates JSON match rules for Reltio configurations.
# It uses OpenAI's GPT-3.5-turbo model to generate match rules based on user input descriptions.
# The script also includes functionality to authenticate with Reltio, retrieve current configurations,
# and update configurations with the generated match rules.
# Developed by : Raj Kumar, Saicharan, Saurabh, Sravya

import streamlit as st
import requests
import json
from requests.auth import HTTPBasicAuth
import base64
import openai
from openai import OpenAI

# Sample JSON match rules for reference
sample_json = [
        {
            "uri": "configuration/entityTypes/HCO/matchGroups/Rule4",
            "label": "Rule4:Exact(CountryCode,Name,SAPID)",
            "type": "automatic",
            "useOvOnly": "true",
            "rule": {
                "ignoreInToken": [
                    "configuration/entityTypes/HCO/attributes/RecordOwner",
                    "configuration/entityTypes/HCO/attributes/Identifiers/attributes/ID",
                    "configuration/entityTypes/HCO/attributes/Identifiers/attributes/Type"
                ],
                "and": {
                    "exact": [
                        "configuration/entityTypes/HCO/attributes/CountryCode",
                        "configuration/entityTypes/HCO/attributes/Name",
                        "configuration/entityTypes/HCO/attributes/Identifiers/attributes/Type",
                        "configuration/entityTypes/HCO/attributes/Identifiers/attributes/ID"
                    ],
                    "equals": [
                        {
                            "value": "France",
                            "uri": "configuration/entityTypes/HCO/attributes/CountryCode"
                        },
                        {
                            "value": "SAP ID",
                            "uri": "configuration/entityTypes/HCO/attributes/Identifiers/attributes/Type"
                        }
                    ],
                    "not": {
                        "and": {
                            "exact": [
                                "configuration/entityTypes/HCO/attributes/RecordOwner"
                            ],
                            "equals": [
                                {
                                    "value": "External",
                                    "uri": "configuration/entityTypes/HCO/attributes/RecordOwner"
                                }
                            ]
                        }
                    }
                }
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/HCP/matchGroups/Rule4",
            "label": "Rule4:Exact(CountryCode,NationalID),Fuzzy(FirstName,LastName)",
            "type": "automatic",
            "useOvOnly": "true",
            "rule": {
                "ignoreInToken": [
                    "configuration/entityTypes/HCP/attributes/Identifiers/attributes/ID",
                    "configuration/entityTypes/HCP/attributes/Identifiers/attributes/Type"
                ],
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        }
                    ]
                },
                "and": {
                    "exact": [
                        "configuration/entityTypes/HCP/attributes/CountryCode",
                        "configuration/entityTypes/HCP/attributes/Identifiers/attributes/Type",
                        "configuration/entityTypes/HCP/attributes/Identifiers/attributes/ID"
                    ],
                    "equals": [
                        {
                            "value": "National ID",
                            "uri": "configuration/entityTypes/HCP/attributes/Identifiers/attributes/Type"
                        }
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/HCP/attributes/FirstName",
                        "configuration/entityTypes/HCP/attributes/LastName"
                    ],
                    "cleanse": [
                        {
                            "cleanseAdapter": "com.reltio.cleanse.impl.NameDictionaryCleanser",
                            "mappings": [
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/FirstName"
                                }
                            ]
                        },
                        {
                            "cleanseAdapter": "com.reltio.cleanse.impl.NameDictionaryCleanser",
                            "mappings": [
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/LastName"
                                }
                            ]
                        }
                    ],
                    "not": {
                        "and": {
                            "exact": [
                                "configuration/sources"
                            ],
                            "equals": [
                                {
                                    "value": "Veeva",
                                    "uri": "configuration/sources"
                                }
                            ]
                        }
                    }
                }
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/ProductGroup/matchGroups/ProductGroupRule1",
            "label": "Rule 1: Automatic ProductGroup match by exact(Name(Country Truncated), Group Type)",
            "type": "automatic",
            "scope": "ALL",
            "useOvOnly": "true",
            "rule": {
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/ProductGroup/attributes/Name",
                            "parameters": [
                                {
                                    "parameter": "groups",
                                    "values": [
                                        {
                                            "className": "com.reltio.match.token.ExactMatchToken",
                                            "sortWords": "false",
                                            "noiseDictionary": "https://s3.amazonaws.com/reltio.match.test/Bayer/Nh5YtmKomhoFnba/bay_cph_pdp_productgroup_noise_dictionary.txt"
                                        }
                                    ]
                                }
                            ],
                            "class": "com.reltio.match.token.CustomMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/ProductGroup/attributes/Name",
                            "parameters": [
                                {
                                    "parameter": "groups",
                                    "values": [
                                        {
                                            "className": "com.reltio.match.comparator.BasicStringComparator",
                                            "sortWords": "false",
                                            "noiseDictionary": "https://s3.amazonaws.com/reltio.match.test/Bayer/Nh5YtmKomhoFnba/bay_cph_pdp_productgroup_noise_dictionary.txt"
                                        }
                                    ]
                                }
                            ],
                            "class": "com.reltio.match.comparator.CustomComparator"
                        }
                    ]
                },
                "and": {
                    "exact": [
                        "configuration/entityTypes/ProductGroup/attributes/Type",
                        "configuration/entityTypes/ProductGroup/attributes/Name"
                    ],
                    "exactOrNull": [
                        "configuration/entityTypes/ProductGroup/attributes/IsMedicalProduct"
                    ]
                }
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/MedicinalProduct/matchGroups/MedicinalProductRule4",
            "label": "Rule 4: Automatic MedicinalProduct match by Exact(Product Name, Country, Source) & ExactORNull(Type,Manuafacturer)",
            "type": "automatic",
            "scope": "ALL",
            "useOvOnly": "true",
            "rule": {
                "and": {
                    "exact": [
                        "configuration/sources",
                        "configuration/entityTypes/MedicinalProduct/attributes/Country",
                        "configuration/entityTypes/MedicinalProduct/attributes/Name"
                    ],
                    "exactOrNull": [
                        "configuration/entityTypes/MedicinalProduct/attributes/Type",
                        "configuration/entityTypes/MedicinalProduct/attributes/Manufacturer"
                    ]
                }
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/Individual/matchGroups/ByName",
            "label": "Automatic individual match by name",
            "type": "automatic",
            "rule": {
                "or" : {
                    "exact": [
                        "configuration/entityTypes/Individual/attributes/FirstName"
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/Individual/attributes/LastName"
                    ]
                }
            }
        },
        {
            "uri": "configuration/entityTypes/Individual/matchGroups/BySSN",
            "label": "Individuals not match by SSN",
            "type": "automatic",
            "negativeRule" : {
                "notExactSame": [
                    "configuration/entityTypes/Individual/attributes/SSN"
                ]
            }
        },
        {
            "uri": "configuration/entityTypes/HCO/matchGroups/Rule1",
            "label": "Rule1:Exact(CountryCode,PostalCode),Fuzzy(Name,AdrLnl,City),EON(State,Specialty)",
            "type": "suspect",
            "useOvOnly": "true",
            "rule": {
                "ignoreInToken": [
                    "configuration/entityTypes/HCO/attributes/Specialities/attributes/Specialty",
                    "configuration/entityTypes/HCO/attributes/RecordOwner"
                ],
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Name",
                            "class": "com.reltio.match.token.BasicTokenizedOrganizationNameMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.token.AddressLineMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/City",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Name",
                            "class": "com.reltio.match.comparator.BasicTokenizedOrganizationNameComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.comparator.AddressLineComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/City",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        }
                    ]
                },
                "and": {
                    "exact": [
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/PostalCode",
                        "configuration/entityTypes/HCO/attributes/CountryCode"
                    ],
                    "exactOrNull": [
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/StateProvince",
                        "configuration/entityTypes/HCO/attributes/Specialities/attributes/Specialty"
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/HCO/attributes/Name",
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/City"
                    ],
                    "not": {
                        "and": {
                            "exact": [
                                "configuration/entityTypes/HCO/attributes/RecordOwner"
                            ],
                            "equals": [
                                {
                                    "value": "External",
                                    "uri": "configuration/entityTypes/HCO/attributes/RecordOwner"
                                }
                            ]
                        }
                    }
                }
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/HCO/matchGroups/Rule2",
            "label": "Rule2:Exact(CountryCode,Name,PostalCode,Identifier),Fuzzy(AdrLnl,City),EON(State)",
            "type": "suspect",
            "scope": "NONE",
            "useOvOnly": "true",
            "rule": {
                "ignoreInToken": [
                    "configuration/entityTypes/HCO/attributes/RecordOwner",
                    "configuration/entityTypes/HCO/attributes/Identifiers/attributes/ID",
                    "configuration/entityTypes/HCO/attributes/Identifiers/attributes/Type"
                ],
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.token.AddressLineMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/City",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.comparator.AddressLineComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/City",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        }
                    ]
                },
                "and": {
                    "exact": [
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/PostalCode",
                        "configuration/entityTypes/HCO/attributes/CountryCode",
                        "configuration/entityTypes/HCO/attributes/Name",
                        "configuration/entityTypes/HCO/attributes/Identifiers/attributes/Type",
                        "configuration/entityTypes/HCO/attributes/Identifiers/attributes/ID"
                    ],
                    "exactOrNull": [
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/StateProvince"
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/City"
                    ],
                    "not": {
                        "and": {
                            "exact": [
                                "configuration/entityTypes/HCO/attributes/RecordOwner"
                            ],
                            "equals": [
                                {
                                    "value": "External",
                                    "uri": "configuration/entityTypes/HCO/attributes/RecordOwner"
                                }
                            ]
                        }
                    }
                }
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/HCO/matchGroups/Rule3",
            "label": "Rule3:Exact(CountryCode,PostalCode),Fuzzy(AdrLnl,City)",
            "type": "suspect",
            "useOvOnly": "true",
            "rule": {
                "ignoreInToken": [
                    "configuration/entityTypes/HCO/attributes/RecordOwner"
                ],
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.token.AddressLineMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/City",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.comparator.AddressLineComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/City",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        }
                    ]
                },
                "and": {
                    "exact": [
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/PostalCode",
                        "configuration/entityTypes/HCO/attributes/CountryCode"
                    ],
                    "equals": [
                        {
                            "value": "Italy",
                            "uri": "configuration/entityTypes/HCO/attributes/CountryCode"
                        }
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/City"
                    ],
                    "not": {
                        "and": {
                            "exact": [
                                "configuration/entityTypes/HCO/attributes/RecordOwner"
                            ],
                            "equals": [
                                {
                                    "value": "External",
                                    "uri": "configuration/entityTypes/HCO/attributes/RecordOwner"
                                }
                            ]
                        }
                    }
                }
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/HCO/matchGroups/TransLiteratorRule1",
            "label": "TransLiterator Rule1:Exact(CountryCode,City),Fuzzy(Name,AdrLnl),EON(State,PostalCode)",
            "type": "suspect",
            "useOvOnly": "true",
            "rule": {
                "ignoreInToken": [
                    "configuration/entityTypes/HCO/attributes/RecordOwner"
                ],
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Name",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "\\W+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                },
                                {
                                    "parameter": "threshold",
                                    "value": "2"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.token.AddressLineMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Name",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                },
                                {
                                    "parameter": "threshold",
                                    "value": "90%"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.comparator.AddressLineComparator"
                        }
                    ]
                },
                "and": {
                    "exact": [
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/City",
                        "configuration/entityTypes/HCO/attributes/CountryCode"
                    ],
                    "equals": [
                        {
                            "value": "China",
                            "uri": "configuration/entityTypes/HCO/attributes/CountryCode"
                        }
                    ],
                    "exactOrNull": [
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/StateProvince",
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/PostalCode"
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/HCO/attributes/Name",
                        "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1"
                    ],
                    "cleanse": [
                        {
                            "cleanseAdapter": "com.reltio.cleanse.impl.TransliterateCleanser",
                            "cleanseAdapterParams": {
                                "transliteratorCommand": "Any-Latin"
                            },
                            "mappings": [
                                {
                                    "attribute": "configuration/entityTypes/HCO/attributes/Name",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCO/attributes/Name"
                                },
                                {
                                    "attribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCO/attributes/Addresses/attributes/AddressLine1"
                                }
                            ]
                        }
                    ],
                    "not": {
                        "and": {
                            "exact": [
                                "configuration/entityTypes/HCO/attributes/RecordOwner"
                            ],
                            "equals": [
                                {
                                    "value": "External",
                                    "uri": "configuration/entityTypes/HCO/attributes/RecordOwner"
                                }
                            ]
                        }
                    }
                }
            },
            "scoreStandalone": 100,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/HCP/matchGroups/Rule1",
            "label": "Rule1:Exact(ContryCode,AdrLn1,City,State,PostalCode,Identifier),Fuzzy(FirstName,LastName),EON(MiddleName,Suffix)",
            "type": "suspect",
            "scope": "NONE",
            "useOvOnly": "true",
            "rule": {
                "ignoreInToken": [
                    "configuration/entityTypes/HCP/attributes/Identifiers/attributes/ID",
                    "configuration/entityTypes/HCP/attributes/RecordOwner",
                    "configuration/entityTypes/HCP/attributes/Identifiers/attributes/Type"
                ],
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        }
                    ]
                },
                "and": {
                    "exact": [
                        "configuration/entityTypes/HCP/attributes/CountryCode"
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/HCP/attributes/FirstName",
                        "configuration/entityTypes/HCP/attributes/LastName"
                    ],
                    "cleanse": [
                        {
                            "cleanseAdapter": "com.reltio.cleanse.impl.NameDictionaryCleanser",
                            "mappings": [
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/FirstName"
                                }
                            ]
                        },
                        {
                            "cleanseAdapter": "com.reltio.cleanse.impl.NameDictionaryCleanser",
                            "mappings": [
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/LastName"
                                }
                            ]
                        }
                    ],
                    "and": {
                        "exact": [
                            "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1",
                            "configuration/entityTypes/HCP/attributes/Addresses/attributes/City",
                            "configuration/entityTypes/HCP/attributes/Addresses/attributes/StateProvince",
                            "configuration/entityTypes/HCP/attributes/Addresses/attributes/PostalCode",
                            "configuration/entityTypes/HCP/attributes/Identifiers/attributes/Type",
                            "configuration/entityTypes/HCP/attributes/Identifiers/attributes/ID"
                        ],
                        "exactOrNull": [
                            "configuration/entityTypes/HCP/attributes/SuffixName",
                            "configuration/entityTypes/HCP/attributes/MiddleName"
                        ]
                    },
                    "not": {
                        "and": {
                            "exact": [
                                "configuration/entityTypes/HCP/attributes/RecordOwner"
                            ],
                            "equals": [
                                {
                                    "value": "External",
                                    "uri": "configuration/entityTypes/HCP/attributes/RecordOwner"
                                }
                            ]
                        }
                    }
                }
            },
            "scoreStandalone": 90,
            "scoreIncremental": 90
        },
        {
            "uri": "configuration/entityTypes/HCP/matchGroups/Rule2",
            "label": "Rule2:Exact(CountryCode,City,State,PostalCode),Fuzzy(FirstName,LastName,AdrLn1),EON(Suffix)",
            "type": "suspect",
            "scope": "NONE",
            "useOvOnly": "true",
            "rule": {
                "ignoreInToken": [
                    "configuration/entityTypes/HCP/attributes/RecordOwner"
                ],
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.token.AddressLineMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.comparator.AddressLineComparator"
                        }
                    ]
                },
                "and": {
                    "exact": [
                        "configuration/entityTypes/HCP/attributes/CountryCode",
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/City",
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/StateProvince",
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/PostalCode"
                    ],
                    "exactOrNull": [
                        "configuration/entityTypes/HCP/attributes/SuffixName"
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/HCP/attributes/FirstName",
                        "configuration/entityTypes/HCP/attributes/LastName",
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1"
                    ],
                    "cleanse": [
                        {
                            "cleanseAdapter": "com.reltio.cleanse.impl.NameDictionaryCleanser",
                            "mappings": [
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/FirstName"
                                }
                            ]
                        },
                        {
                            "cleanseAdapter": "com.reltio.cleanse.impl.NameDictionaryCleanser",
                            "mappings": [
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/LastName"
                                }
                            ]
                        }
                    ],
                    "not": {
                        "and": {
                            "exact": [
                                "configuration/entityTypes/HCP/attributes/RecordOwner"
                            ],
                            "equals": [
                                {
                                    "value": "External",
                                    "uri": "configuration/entityTypes/HCP/attributes/RecordOwner"
                                }
                            ]
                        }
                    }
                }
            },
            "scoreStandalone": 60,
            "scoreIncremental": 70
        },
        {
            "uri": "configuration/entityTypes/HCP/matchGroups/Rule3",
            "label": "Rule3:Exact(CountryCode,FirstName,LastName,City,State,PostalCode),Fuzzy(AdrLn1),EON(MiddleName,Suffix)",
            "type": "suspect",
            "scope": "NONE",
            "useOvOnly": "true",
            "rule": {
                "ignoreInToken": [
                    "configuration/entityTypes/HCP/attributes/RecordOwner"
                ],
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.token.AddressLineMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.comparator.AddressLineComparator"
                        }
                    ]
                },
                "and": {
                    "exact": [
                        "configuration/entityTypes/HCP/attributes/FirstName",
                        "configuration/entityTypes/HCP/attributes/LastName",
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/City",
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/StateProvince",
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/PostalCode",
                        "configuration/entityTypes/HCP/attributes/CountryCode"
                    ],
                    "exactOrNull": [
                        "configuration/entityTypes/HCP/attributes/SuffixName",
                        "configuration/entityTypes/HCP/attributes/MiddleName"
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1"
                    ],
                    "not": {
                        "and": {
                            "exact": [
                                "configuration/entityTypes/HCP/attributes/RecordOwner"
                            ],
                            "equals": [
                                {
                                    "value": "External",
                                    "uri": "configuration/entityTypes/HCP/attributes/RecordOwner"
                                }
                            ]
                        }
                    }
                }
            },
            "scoreStandalone": 20,
            "scoreIncremental": 60
        },
        {
            "uri": "configuration/entityTypes/HCP/matchGroups/Rule5",
            "label": "Rule5:Fuzzy(FirstName,LastName),((Exact(CountryCode,City,State,PostalCode),Fuzzy(AdrLn1),EON(Suffix)) or Exact(Email))",
            "type": "suspect",
            "useOvOnly": "true",
            "rule": {
                "ignoreInToken": [
                    "configuration/entityTypes/HCP/attributes/RecordOwner"
                ],
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.token.AddressLineMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.comparator.AddressLineComparator"
                        }
                    ]
                },
                "and": {
                    "fuzzy": [
                        "configuration/entityTypes/HCP/attributes/FirstName",
                        "configuration/entityTypes/HCP/attributes/LastName"
                    ],
                    "cleanse": [
                        {
                            "cleanseAdapter": "com.reltio.cleanse.impl.NameDictionaryCleanser",
                            "mappings": [
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/FirstName"
                                }
                            ]
                        },
                        {
                            "cleanseAdapter": "com.reltio.cleanse.impl.NameDictionaryCleanser",
                            "mappings": [
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/LastName"
                                }
                            ]
                        }
                    ],
                    "or": {
                        "exact": [
                            "configuration/entityTypes/HCP/attributes/Email/attributes/Email"
                        ],
                        "and": {
                            "exact": [
                                "configuration/entityTypes/HCP/attributes/CountryCode",
                                "configuration/entityTypes/HCP/attributes/Addresses/attributes/City",
                                "configuration/entityTypes/HCP/attributes/Addresses/attributes/StateProvince",
                                "configuration/entityTypes/HCP/attributes/Addresses/attributes/PostalCode"
                            ],
                            "exactOrNull": [
                                "configuration/entityTypes/HCP/attributes/SuffixName"
                            ],
                            "fuzzy": [
                                "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1"
                            ]
                        }
                    },
                    "not": {
                        "and": {
                            "exact": [
                                "configuration/entityTypes/HCP/attributes/RecordOwner"
                            ],
                            "equals": [
                                {
                                    "value": "External",
                                    "uri": "configuration/entityTypes/HCP/attributes/RecordOwner"
                                }
                            ]
                        }
                    }
                }
            },
            "scoreStandalone": 60,
            "scoreIncremental": 70
        },
        {
            "uri": "configuration/entityTypes/HCP/matchGroups/TransLiteratorRule1",
            "label": "TransLiterator Rule1:Exact(CountryCode),Fuzzy(FirstName,LastName,AdrLn1),EON(Suffix,City,State,PostalCode)",
            "type": "suspect",
            "scope": "NONE",
            "useOvOnly": "true",
            "rule": {
                "ignoreInToken": [
                    "configuration/entityTypes/HCP/attributes/RecordOwner"
                ],
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.token.DistinctWordsMatchToken"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.token.AddressLineMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                            "parameters": [
                                {
                                    "parameter": "pattern",
                                    "value": "[a-zA-Z]+"
                                },
                                {
                                    "parameter": "useStemmer",
                                    "value": "true"
                                },
                                {
                                    "parameter": "useSoundex",
                                    "value": "true"
                                }
                            ],
                            "class": "com.reltio.match.comparator.DistinctWordsComparator"
                        },
                        {
                            "attribute": "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1",
                            "class": "com.reltio.match.comparator.AddressLineComparator"
                        }
                    ]
                },
                "and": {
                    "exact": [
                        "configuration/entityTypes/HCP/attributes/CountryCode"
                    ],
                    "equals": [
                        {
                            "value": "China",
                            "uri": "configuration/entityTypes/HCP/attributes/CountryCode"
                        }
                    ],
                    "exactOrNull": [
                        "configuration/entityTypes/HCP/attributes/SuffixName",
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/City",
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/StateProvince",
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/PostalCode"
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/HCP/attributes/FirstName",
                        "configuration/entityTypes/HCP/attributes/LastName",
                        "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1"
                    ],
                    "cleanse": [
                        {
                            "cleanseAdapter": "com.reltio.cleanse.impl.NameDictionaryCleanser",
                            "mappings": [
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/FirstName"
                                },
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/LastName"
                                }
                            ]
                        },
                        {
                            "cleanseAdapter": "com.reltio.cleanse.impl.TransliterateCleanser",
                            "cleanseAdapterParams": {
                                "transliteratorCommand": "Any-Latin"
                            },
                            "mappings": [
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/FirstName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/FirstName"
                                },
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/LastName",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/LastName"
                                },
                                {
                                    "attribute": "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1",
                                    "mandatory": "false",
                                    "allValues": "false",
                                    "cleanseAttribute": "configuration/entityTypes/HCP/attributes/Addresses/attributes/AddressLine1"
                                }
                            ]
                        }
                    ],
                    "not": {
                        "and": {
                            "exact": [
                                "configuration/entityTypes/HCP/attributes/RecordOwner"
                            ],
                            "equals": [
                                {
                                    "value": "External",
                                    "uri": "configuration/entityTypes/HCP/attributes/RecordOwner"
                                }
                            ]
                        }
                    }
                }
            },
            "scoreStandalone": 100,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/ProductGroup/matchGroups/ProductGroupRule2",
            "label": "Rule 2: Suspect ProductGroup match by fuzzy(Name) & exact(Group Type)",
            "type": "suspect",
            "rule": {
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/ProductGroup/attributes/Name",
                            "class": "com.reltio.match.token.FuzzyTextMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/ProductGroup/attributes/Name",
                            "class": "com.reltio.match.comparator.MetaphoneComparator"
                        }
                    ]
                },
                "and": {
                    "exact": [
                        "configuration/entityTypes/ProductGroup/attributes/Type"
                    ],
                    "exactOrNull": [
                        "configuration/entityTypes/ProductGroup/attributes/IsMedicalProduct"
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/ProductGroup/attributes/Name"
                    ]
                }
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/MedicinalProduct/matchGroups/MedicinalProductNegRule1",
            "label": "Neg Rule1: Products should not match or they are in different countries.",
            "type": "suspect",
            "negativeRule": {
                "notExactSame": [
                    "configuration/entityTypes/MedicinalProduct/attributes/Country"
                ]
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/MedicinalProduct/matchGroups/MedicinalProductRule1",
            "label": "Rule 1: Suspect MedicinalProduct match by exact(ID)",
            "type": "suspect",
            "rule": {
                "and": {
                    "exact": [
                        "configuration/entityTypes/MedicinalProduct/attributes/Identifiers/attributes/Type",
                        "configuration/entityTypes/MedicinalProduct/attributes/Identifiers/attributes/ID",
                        "configuration/entityTypes/MedicinalProduct/attributes/Country"
                    ],
                    "exactOrNull": [
                        "configuration/entityTypes/MedicinalProduct/attributes/Identifiers/attributes/CountryCode"
                    ]
                }
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/MedicinalProduct/matchGroups/MedicinalProductRule2",
            "label": "Rule 2: Suspect MedicinalProduct match by exact(Product Name)",
            "type": "suspect",
            "rule": {
                "and": {
                    "exact": [
                        "configuration/entityTypes/MedicinalProduct/attributes/Name",
                        "configuration/entityTypes/MedicinalProduct/attributes/Country"
                    ]
                }
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/MedicinalProduct/matchGroups/MedicinalProductRule3",
            "label": "Rule 3: Suspect MedicinalProduct match by fuzzy(Product Name) & exact(Strength)",
            "type": "suspect",
            "scope": "ALL",
            "useOvOnly": "true",
            "rule": {
                "matchTokenClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/MedicinalProduct/attributes/Name",
                            "class": "com.reltio.match.token.FuzzyTextMatchToken"
                        }
                    ]
                },
                "comparatorClasses": {
                    "mapping": [
                        {
                            "attribute": "configuration/entityTypes/MedicinalProduct/attributes/Name",
                            "class": "com.reltio.match.comparator.MetaphoneComparator"
                        }
                    ]
                },
                "and": {
                    "exactOrNull": [
                        "configuration/entityTypes/MedicinalProduct/attributes/Strength/attributes/Name",
                        "configuration/entityTypes/MedicinalProduct/attributes/Dose",
                        "configuration/entityTypes/MedicinalProduct/attributes/Country"
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/MedicinalProduct/attributes/Name"
                    ]
                }
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/ProductGroup/matchGroups/test123",
            "label": "test123",
            "type": "relevance_based",
            "scope": "INTERNAL",
            "useOvOnly": "true",
            "rule": {
                "and": {
                    "exact": [
                        "configuration/entityTypes/ProductGroup/attributes/BayerID",
                        "configuration/entityTypes/ProductGroup/attributes/Name"
                    ],
                    "fuzzy": [
                        "configuration/entityTypes/ProductGroup/attributes/AlternateName/attributes/Country"
                    ]
                },
                "actionThresholds": [
                    {
                        "type": "auto_match",
                        "threshold": "0.5-1"
                    },
                    {
                        "type": "potential_match",
                        "threshold": "0-0.5"
                    }
                ]
            },
            "scoreStandalone": 0,
            "scoreIncremental": 0
        },
        {
            "uri": "configuration/entityTypes/HCP/matchGroups/ByNames",
            "label": "By Names",
            "type": "relevance_based",
            "rule": {
                "and": {
                    "exact": [
                        "configuration/entityTypes/HCP/attributes/FirstName",
                        "configuration/entityTypes/HCP/attributes/LastName"
                    ],
                    "exactOrAllNull": [
                        "configuration/entityTypes/HCP/attributes/Suffix"
                    ]
                },
                "weights": [
                    {
                        "attribute": "configuration/entityTypes/HCP/attributes/Suffix",
                        "weight": 0.2
                    }
                ],
                "actionThresholds": [
                    {
                        "type": "auto_merge",
                        "threshold": "0.8-1.0"
                    },
                    {
                        "type": "potential_match",
                        "threshold": "0.4-0.8"
                    }
                ],
                "matchTokenClass": "com.reltio.match.token.ExactMatchToken"
            },
            "matchServiceClass": "com.reltio.businesslogic.match.providers.internal.InternalMatchService"
        },
        {
            "uri": "configuration/entityTypes/HCP/matchGroups/PotentialMatchByEmail",
            "label": "By Email",
            "type": "relevance_based",
            "rule": {
              "and": {
                "fuzzy": [
                  "configuration/entityTypes/HCP/attributes/Email/attributes/Email"
                ]
              },
              "actionThresholds": [
                {
                  "type": "auto_match",
                  "threshold": "0.99-1",
                  "label": "candidate for merge"
                },
                {
                  "type": "potential_match",
                  "threshold": "0.9-0.99",
                  "label": "suspect match for review"
                }
              ]
            }
          }
]


def generate_match_rule(user_input, client):
    """
    Generates a JSON match rule based on user input description using OpenAI's GPT-3.5-turbo model.
    """
    try:
        reltio_docs_url = "https://docs.reltio.com/"
        
        prompt = (
            f"Based on the following description, generate a JSON match rule similar to the list of sample:\n"
            f"Sample JSON: {json.dumps(sample_json, indent=2)}\n"
            f"Description: {user_input}\n"
            f"Refer to the Reltio documentation for more precise JSON formatting: {reltio_docs_url}"
        )
        response = client.chat.completions.create(            
            model="gpt-3.5-turbo",            
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.6    
        )        
        match_rule_json = response.choices[0].message.content.strip()        

        try:
            match_rule_dict = json.loads(match_rule_json)
            return json.dumps(match_rule_dict, indent=4)
        except json.JSONDecodeError:
            return "Failed to generate valid JSON."
    except Exception as e:
        return f"Error: {e}"

def get_access_token(auth_url, auth_url_body, auth_url_headers):
    """
    Retrieves an access token from the Reltio authentication service.
    """
    try:
        response = requests.post(auth_url, data=auth_url_body, headers=auth_url_headers)
        if response.status_code == 200:
            login_access = response.json()
            return login_access.get("access_token")
        else:
            st.error(f"Failed to get access token. Status code: {response.status_code}, Response: {response.text}")
            return None
    except Exception as e:
        st.error(f"Error: {e}")
        return None

def get_l3_configuration(reltio_api_url, access_token):
    """
    Retrieves the current L3 configuration from the Reltio API.
    """
    try:
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        response = requests.get(reltio_api_url, headers=headers)
        
        if response.status_code == 200:
            l3_configuration = response.json()
            return l3_configuration
        else:
            return f"Failed to get L3 configuration. Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return f"Error: {e}"

def update_l3_configuration(reltio_api_put, access_token, new_configuration):
    """
    Updates the L3 configuration on the Reltio API with the new configuration.
    """
    try:
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
        response = requests.put(reltio_api_put, headers=headers, data=json.dumps(new_configuration))
        
        if response.status_code == 200:
            return "L3 configuration updated successfully."
        elif response.status_code == 202:
            return "L3 configuration updated successfully."
        else:
            return f"Failed to update L3 configuration. Status code: {response.status_code}, Response: {response.text}"
    except Exception as e:
        return f"Error: {e}"

def main():
    """
    Main function to run the Streamlit application.
    """
    st.title("Reltio Match Rule Generator")
    
    reltio_api_url = st.text_input("Enter Reltio API URL:")
    reltio_api_put = st.text_input("Enter Reltio API PUT URL:")
    reltio_client_id = st.text_input("Enter Reltio Client ID:")
    reltio_client_secret = st.text_input("Enter Reltio Client Secret:")
    openai_api_key = st.text_input("Enter OpenAI API Key:")
    
    if st.button("Set API Keys"):
        auth_url = "https://auth.reltio.com/oauth/token"
        auth_url_body = "grant_type=client_credentials"
        auth_url_headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        auth_header_value = base64.b64encode(f"{reltio_client_id}:{reltio_client_secret}".encode()).decode()
        auth_url_headers["Authorization"] = f"Basic {auth_header_value}"
        
        client = OpenAI(api_key=openai_api_key)
        
        st.session_state['auth_url'] = auth_url
        st.session_state['auth_url_body'] = auth_url_body
        st.session_state['auth_url_headers'] = auth_url_headers
        st.session_state['client'] = client
        st.session_state['reltio_api_url'] = reltio_api_url
        st.session_state['reltio_api_put'] = reltio_api_put

    if 'client' in st.session_state:
        user_input = st.text_area("Enter your description for the match rule:")
        if st.button("Generate JSON"):
            bot_response = generate_match_rule(user_input, st.session_state['client'])
            st.session_state['bot_response'] = bot_response
            st.session_state['action'] = None

        if 'bot_response' in st.session_state:
            st.text_area("Generated JSON:", value=st.session_state['bot_response'], height=300)
            
            action = st.selectbox("Select an action:", ["Select an action", "Continue with the generated JSON", "Edit the generated JSON", "Generate another JSON"], key='action')
            
            if action == "Edit the generated JSON":
                st.session_state['bot_response'] = st.text_area("Edit the generated JSON:", value=st.session_state['bot_response'], height=300)
                try:
                    json.loads(st.session_state['bot_response'])  # Validate JSON
                except json.JSONDecodeError:
                    st.error("Invalid JSON. Please try again.")
                    return
            
            if action == "Generate another JSON":
                st.session_state.pop('bot_response')
                st.experimental_rerun()
            
            if action == "Continue with the generated JSON" or action == "Edit the generated JSON":
                append_action = st.selectbox("Do you want to append the generated JSON to the L3 configuration?", ["Select an option", "Yes", "No"], key='append_action')
                if append_action == "Yes":
                    entitytype = st.text_input("Enter the entity type to append the JSON to (e.g., HCO):")
                    if st.button("Append JSON"):
                        access_token = get_access_token(st.session_state['auth_url'], st.session_state['auth_url_body'], st.session_state['auth_url_headers'])
                        if access_token:
                            l3_config = get_l3_configuration(st.session_state['reltio_api_url'], access_token)
                            if isinstance(l3_config, dict):
                                for i in l3_config['entityTypes']:
                                    for j in i.keys():
                                        if j == 'uri':
                                            entity = i[j].split('/')[-1]
                                            if entity == entitytype:
                                                i['matchGroups'].append(json.loads(st.session_state['bot_response']))
                                new_configuration = l3_config
                                update_response = update_l3_configuration(st.session_state['reltio_api_put'], access_token, new_configuration)
                                st.write(update_response)
                            else:
                                st.error(l3_config)
                        else:
                            st.error("Failed to obtain access token.")
                elif append_action == "No":
                    st.write("JSON not appended to L3 configuration.")

if __name__ == "__main__":
    main()