# DRB Sentinel-2 Metadata AddOn
This addon allowing to enrich the `Sentinel-2 Product` topic with its metadata
derivative topics also. 


Defined metadata:


| e0750a16-f302-11ec-b939-0242ac120002 -- Sentinel-2 User Product |
|-----------------------------------------------------------------|
| platformShortName                                               |
| platformSerialIdentifier                                        |
| instrumentShortName                                             |
| sensorType                                                      |
| operationalMode                                                 |
| processingLevel                                                 |
| processingDate                                                  |
| beginningDateTime                                               |
| endingDateTime                                                  |
| orbitNumber)                                                    |
| orbitDirection                                                  |
| relativeOrbitNumber                                             |
| coordinates                                                     |
| cloudCover                                                      |
| productType                                                     |
| filename                                                        |
| format                                                          |
| spacecraftName                                                  |
| processingBaseline                                              |
| dataTakeSensingStart                                            |
| datastripSensingStart                                           |
| datastripSensingStop                                            |
| degradedAncillaryDataPercentage                                 |
| degradedMSIDataPercentage                                       |
| sensorQualityFlag                                               |
| geometricQualityFlag                                            |
| generalQualityFlag                                              |
| formatCorrectnessFlag                                           |
| radiometricQualityFlag                                          |
| granuleIdentifier                                               |

| 242ce8e2-e1af-11ec-8fea-0242ac120002 Sentinel-2 Level-1c Product |
|------------------------------------------------------------------|
| tileIdentifier                                                   |
| orderedTileIdentifier                                            |

| 73b017d6-e1af-11ec-8fea-0242ac120002 Sentinel-2 Level-2a Product |
|------------------------------------------------------------------|
| noDataPixelPercentage                                            |
| saturatedDefectivePixelPercentage                                |
| darkFeaturesPercentage                                           |
| cloudShadowPercentage                                            |
| vegetationPercentage                                             |
| notVegetatedPercentage                                           |
| waterPercentage                                                  |
| unclassifiedPercentage                                           |
| mediumProbaCloudsPercentage                                      |
| highProbaCloudsPercentage                                        |
| thinCirrusPercentage                                             |
| snowIcePercentage                                                |
| radiativeTransferAccuracy                                        |
| waterVapourRetrievalAccuracy                                     |
| aotRetrievalAccuracy                                             |

| fad132d2-f2fc-11ec-b939-0242ac120002 Sentinel-2 Datastrip |
|-----------------------------------------------------------|
| platformShortName                                         |
| platformSerialIdentifier                                  |
| instrumentShortName                                       |
| operationalMode                                           |
| processingDate                                            |
| processingCenter                                          |
| processorVersion                                          |
| beginningDateTime                                         |
| endingDateTime                                            |
| orbitNumber                                               |
| relativeOrbitNumber                                       |
| coordinates                                               |
| productType                                               |
| qualityStatus                                             |
| qualityInfo                                               |
| productGroupId                                            |

| c6da0d68-f23a-11ec-b939-0242ac120002 Sentinel-2 Granule |
|---------------------------------------------------------|
| platformShortName                                       |
| platformName                                            |
| platformSerialIdentifier                                |
| instrumentShortName                                     |
| processingDate                                          |
| processingCenter                                        |
| processorVersion                                        |
| beginningDateTime                                       |
| endingDateTime                                          |
| orbitNumber                                             |
| coordinates                                             |
| cloudCover                                              |
| productType                                             |
| qualityStatus                                           |
| qualityInfo                                             |
| datastripId                                             |
| productGroupId                                          |
| tileId                                                  |
| illuminationZenithAngle                                 |

| 3f43fa3e-f2f9-11ec-b939-0242ac120002 Sentinel-2 Level-0 HKTM |
|--------------------------------------------------------------|
| platformShortName                                            |
| platformSerialIdentifier                                     |
| instrumentShortName                                          |
| processingDate                                               |
| processingCenter                                             |
| beginningDateTime                                            |
| endingDateTime                                               |
| orbitNumber                                                  |
| lastOrbitNumber                                              |
| relativeOrbitNumber                                          |
| productType                                                  |

| be45c266-f23d-11ec-b939-0242ac120002 Sentinel-2 Auxiliary SAD PDI |
|-------------------------------------------------------------------|
| platformName                                                      |
| platformShortName                                                 |
| platformSerialIdentifier                                          |
| platformShortName                                                 |
| processingDate                                                    |
| processingCenter                                                  |
| beginningDateTime                                                 |
| endingDateTime                                                    |
| orbitNumber                                                       |
| lastOrbitNumber                                                   |
| productType                                                       |
| qualityStatus                                                     |
| qualityInfo                                                       |

| ff9720b6-f2f1-11ec-b939-0242ac120002 Sentinel-2 Level-1C Tile Image File |
|--------------------------------------------------------------------------|
| platformName                                                             |
| platformSerialIdentifier                                                 |
| instrumentShortName                                                      |
| processingDate                                                           |
| processingCenter                                                         |
| processorVersion                                                         |
| beginningDateTime                                                        |
| endingDateTime                                                           |
| orbitNumber                                                              |
| coordinates                                                              |
| cloudCover                                                               |
| qualityStatus                                                            |
| qualityInfo                                                              |
| tileId                                                                   |
| productGroupId                                                           |
| productTypedata                                                          |

| 7de4ab0c-fd40-11ec-b939-0242ac120002 Sentinel-2 Auxiliary GIP |
|---------------------------------------------------------------|
| platformShortName                                             |
| platformSerialIdentifier                                      |
| processingDate                                                |
| processingCenter                                              |
| processorVersion                                              |
| beginningDateTime                                             |
| Value_beginningDateTime_gippTgz                               |
| endingDateTime                                                |
| productType                                                   |

| 0cacd114-0c20-11ed-861d-0242ac120002 Sentinel-2 TGZ AUX_ECMWFD and AUX_UT1UTC |
|-------------------------------------------------------------------------------|
| processingDate                                                                |
| processingCenter                                                              |
| processorVersion                                                              |
| beginningDateTime                                                             |
| endingDateTime                                                                |
| productType                                                                   |

| 8bc2ca58-0c25-11ed-861d-0242ac120002 Sentinel-2 AUX RESORB & PREORB EOF |
|-------------------------------------------------------------------------|
| platformShortName                                                       |
| platformSerialIdentifier                                                |
| processingDate                                                          |
| processingCenter                                                        |
| processorVersion                                                        |
| beginningDateTime                                                       |
| endingDateTime                                                          |
| productType                                                             |
