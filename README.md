# Flood-Monitoring

This application allows an individual to query the UK Environment Agency Real Time flood-monitoring API. The user should select a measurement station from the Environment Agency and the application will display graphs for all the measurements taken by that station over the last 24 hours.

## Requirements

The application consists of a single python script to be run from command line. To visualize outputs, user system must be able to display visual output with DirectX or any other tool that allows for matplotlib visualization.

The only non-standard module requirements for running the application are matplotlib and numpy.

## Usage

The stations are inputted by the user using the corresponing station reference as text. The application provides a helper tool to find measurement stations based on their label, the river they cover, or their RLOIid. The helper tool is case-sensitive, so the user must select the query type (RIVER, LABEL, RLOIid) exactly as written by the helper tool.

After selecting the query type, the user should make the corresponding query, as indicated by the application. The helper tool would then either list all the stations matching the query (if the query is correct), or list a partial list of all available stations.

The user is also able to input the station reference directly as a command line argument in order to skip the station finder altogether. The first command line argument would be taken as the station reference, any other arguments will be ignored.