
'''
DFTB+ input keywords and type
Keywords are restricted to CamelCase as written in official manual
'''
type_key = { 
             'float' : { 
                         'SCCTolerance',
                         'Temperature',
                         'MixingParameter',
                        },
             'int': {
                         'ParserVersion',
                         'MaxSCCIterations',
                         'CachedIterations',
                        },
             'str': { 
                         'Prefix', 
                         'Separator', 
                         'Suffix', 
                         'Atoms',
                         'Label',
                        },
             'bool': {
                         'SCC',
                         'ShellResolved',
                         'OrbitalResolved',
                        },
            }

# build inverse relation
key_type = {value: key for key, values in type_key.items() for value in values}

special_blocks = [ # keywords with content not suitable for recursive dictionary parsing  
        'Geometry', # Gen form or read isolated file
        'MaxAngularMomentum', # Keys are atomic symbols, value could be complicated
        'ProjectStates',  # Repeated 'Region' key
        'KPointsAndWeights', # lines of arrays
        ]

