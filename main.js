// Building Bar graphs in Australia using Vizicities
//This JS script maps linked ABS SDMX to PSMA Beta Builsing and Beta Address APIs.

//Hard coded focus point.  Next step would be dynamic centering on focuspoint.json created by buildingToSA1.py

focuslat =  -34.954350
focuslong = 138.586377
var coords = [focuslat, focuslong];  //149.084785835, -35.3589395509999 // (-34.954350,138.586377)

var world = VIZI.world('world', {
  skybox: true, // cast shadow nad sun
  postProcessing: true
}).setView(coords);

// Add controls
VIZI.Controls.orbit().addTo(world);


// Set position of sun in sky
world._environment._skybox.setInclination(0.2);  // 0.5 is sunset 0.1 is day light. 




// Chroma scale for height-based colours
//var colourScale = chroma.scale(['lightyellow', 'navy']).domain([1,5]);

//var colourScale = chroma.scale('YlOrBr').domain([1,5]);

//VIZI.geoJSONLayer('http://ldap0010:121/1stCutGraphElementsJosn.geojsonSub9.json'
VIZI.imageTileLayer('http://{s}.basemaps.cartocdn.com/light_nolabels/{z}/{x}/{y}.png', {
  attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, &copy; <a href="http://cartodb.com/attributions">CartoDB</a>'
}).addTo(world);

// Chroma scale for height-based colours
var colourScale = chroma.scale('YlOrBr').domain([0,200]);


// Mapzen GeoJSON tile including points, linestrings and polygons
VIZI.geoJSONLayer('/buildingradius.json', {
  output: true,
  interactive: true,
  style: function(feature) {
    var height;
	var colour;
	var colHolder;
  
  // colHolder = feature.properties.RF_TYP
  
    if (feature.properties.MAX_HG2) {
      height = feature.properties.MAX_HG2;
    } else {
      //height = 1 + Math.random() * 100;
    }
	
	if (feature.properties.Country_Total) {
       //colour = '#521421';
       colHolder = feature.properties.Country_Total * 10
       colour = colourScale(colHolder).hex()
       
     }
   
    
  
    //var colour = colourScale(height).hex();

    return {
      color: colour,
      height: height
    };

  },
  filter: function(feature) {
    // Don't show points
    return feature.geometry.type !== 'Point';
  },

onEachFeature: function(feature, layer) {
    layer.on('click', function(layer, point2d, point3d, intersects) {
      var totalpersons = layer.feature.properties.MAX_HG2;
      var Country_Total = layer.feature.properties.Country_Total;
      var Focus_Nationality = layer.feature.properties.Country
      var focuslat2 = focuslat
      //var value = layer.feature.properties.POPDEN;

      //console.log(id + ': ' + value, layer, point2d, point3d, intersects);
      console.log("-----------------------")
      console.log(focuslat2)
      console.log("Total Persons")
      console.log(totalpersons)
      console.log(Focus_Nationality)
      console.log(Country_Total)

    });
  }


  //attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors, <a href="http://whosonfirst.mapzen.com#License">Who\'s On First</a>.'
}).addTo(world);


