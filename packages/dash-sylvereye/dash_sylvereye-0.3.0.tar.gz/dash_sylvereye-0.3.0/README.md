**Dash Sylvereye** is a Dash component library for producing interactive visualizations of large primal road networks on top of web tiled maps.

## Documentation

Coming soon.

## Running the examples

Start by cloning this repository:

````
git clone https://github.com/observatoriogeo/dash-sylvereye.git
cd dash-sylvereye/examples
````

Next, create a virtual environment and install the Python dependencies:

````
python -m venv venv && . venv/bin/activate
pip install -r requirements-examples.txt
````

Finally, try to run an example:

````
cd examples
python 01_VisualizeNetwork.py
````

If you visit http://127.0.0.1:8050/ in your browser, you should see a Dash Sylvereye visualization.

## Build instructions

Start by cloning this repository:

````
git clone https://github.com/observatoriogeo/dash-sylvereye.git
cd dash-sylvereye
````

Next, create a virtual environment and install the Python dependencies:

````
python -m venv venv && . venv/bin/activate
pip install -r requirements-dev.txt
````

Finally, install packages via npm (ignore errors) and run the build script,

````
npm i --ignore-scripts 
npm run build
````
