
var container, camera, scene, renderer, controls;
var geometry, material, points;

var positions = [];
var spheres = [];
init();
animate();
function set_ambient_lighting(ambient_light)
{
  // Add ambient light to the scene
  const ambientLight = new THREE.AmbientLight(ambient_light.color, ambient_light.intensity); // Adjust the intensity as needed
  scene.add(ambientLight);
  console.log("[INFI] Setting ambient light");
}
function set_directional_lighting(directional_light)
{
  console.log("[INFI] Setting directional light");
  // Add directional light to the scene
  const directionalLight = new THREE.DirectionalLight(directional_light.color, directional_light.intensity); // Adjust the intensity as needed
  directionalLight.position.set(0, 1, 0); // Set the position of the light
  scene.add(directionalLight);
}
function add_point_cloud_to_scene(point_cloud)
{
    //const data = event.target.result; // The loaded file data
    // Process the point cloud data here

    // Example: Create a geometry and material for the point cloud
    const geometry = new THREE.BufferGeometry();
    const material = new THREE.MeshStandardMaterial({ color: 0xffffff });

    // Example: Parse the point cloud data and populate the geometry
    const positions = []; // Array to hold the point positions
    // Parse the data and extract the point positions into the positions array
    // Assuming the point cloud data is in a specific format, adjust the parsing logic accordingly
    // Example:
    
    for (let i = 0; i < point_cloud.length; i++) {
        var x = point_cloud[i][0];
        var y = point_cloud[i][1];
        var z = point_cloud[i][2];
        positions.push(x, y, z);
    }
    // Set the positions as an attribute of the geometry
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

    // Create spheres based on the positions
    const radius = 0.1; // Adjust the radius of the spheres as needed
    const sphereGeometry = new THREE.SphereGeometry(radius, 32, 32);
    const spheres = new THREE.Group();

    for (let i = 0; i < positions.length; i += 3) {
        const sphere = new THREE.Mesh(sphereGeometry, material);
        sphere.position.set(positions[i], positions[i + 1], positions[i + 2]);
        spheres.add(sphere);
    }

    // Add the spheres to the scene
    scene.add(spheres);
}
function load_scene(data,point_cloud_count)
{
  console.log("Loading scene...\n");
  console.log(data);
  // set lighting
  //set_ambient_lighting();
  // for each point cloud
  for(var i = 0; i < point_cloud_count;i++)
  {
      add_point_cloud_to_scene(data[i]);
  }

}
function showNotification(message, type = 'info') {
  const notificationContainer = document.getElementById('notification-container');
  
  // Create the notification element
  const notification = document.createElement('div');
  notification.classList.add('alert', `alert-${type}`, 'alert-dismissible', 'fade', 'show');
  notification.setAttribute('role', 'alert');

  // Add the message to the notification
  notification.innerText = message;

  // Add the close button to the notification
  const closeButton = document.createElement('button');
  closeButton.classList.add('btn-close');
  closeButton.setAttribute('type', 'button');
  closeButton.setAttribute('data-bs-dismiss', 'alert');
  closeButton.setAttribute('aria-label', 'Close');
  notification.appendChild(closeButton);

  // Add the notification to the container
  notificationContainer.appendChild(notification);
}
function init() {
  
  //container = document.createElement( 'div' );
  container = document.getElementById("container");
  document.body.appendChild( container );

  camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    1000
  );
      camera.position.z = 5;

    // Add ambient light to the scene

  scene = new THREE.Scene();
  scene.background = new THREE.Color( 0x050505 );

  // add an axis with visible origin
  var axesHelper = new THREE.AxesHelper(100);
  scene.add( axesHelper );

  // Create a random number of spheres with random positions and colors
  /*
  const numSpheres = Math.floor( Math.random() * 100) + 1;
  for (let i = 0; i < numSpheres; i++) {
    const geometry = new THREE.SphereGeometry(0.5, 32, 32);
    var c = 0xffffff;
    console.log("Color "+c);
    const material = new THREE.MeshStandardMaterial({
      color: c,
    });
    const sphere = new THREE.Mesh(geometry);
    sphere.position.set(
      Math.random() * 10 - 5,
      Math.random() * 10 - 5,
      Math.random() * 10 - 5
    );
    scene.add(sphere);
    spheres.push(sphere);
  }
  */
  renderer = new THREE.WebGLRenderer( { antialias: true } );
  renderer.setPixelRatio( window.devicePixelRatio );
  renderer.setSize( window.innerWidth, window.innerHeight );
  container.appendChild( renderer.domElement );
        controls = new THREE.OrbitControls(camera, renderer.domElement);
        controls.enableZoom = true;
  window.addEventListener( 'resize', onWindowResize, false );

}

function onWindowResize() {

  camera.aspect = window.innerWidth / window.innerHeight;
  camera.updateProjectionMatrix();

  renderer.setSize( window.innerWidth, window.innerHeight );

}

function animate() {
    requestAnimationFrame(animate);

    // Rotate the spheres
    spheres.forEach((sphere) => {
      sphere.rotation.x += 0.01;
      sphere.rotation.y += 0.01;
    });

    renderer.render(scene, camera);
  }



// Add an event listener to the container element for file drag and drop
container.addEventListener('dragover', handleDragOver, false);
container.addEventListener('drop', handleFileDrop, false);

function handleDragOver(event) {
  event.stopPropagation();
  event.preventDefault();
  event.dataTransfer.dropEffect = 'copy'; // Set drop effect to copy
}

function handleFileDrop(event) {
  event.stopPropagation();
  event.preventDefault();

  const files = event.dataTransfer.files;
  if (files.length > 0) {
    const file = files[0];
    const reader = new FileReader();
    reader.addEventListener('load', handleFileLoad, false);
    reader.readAsText(file); // Read the file as text
  }
}

function handleFileLoad(event) {
    const data = event.target.result; // The loaded file data
    // Process the point cloud data here

    // Example: Create a geometry and material for the point cloud
    const geometry = new THREE.BufferGeometry();
    const material = new THREE.MeshStandardMaterial({ color: 0xffffff });

    // Example: Parse the point cloud data and populate the geometry
    const positions = []; // Array to hold the point positions
    // Parse the data and extract the point positions into the positions array
    // Assuming the point cloud data is in a specific format, adjust the parsing logic accordingly
    // Example:
    const lines = data.split('\n');
    for (let i = 0; i < lines.length; i++) {
        const values = lines[i].trim().split(' ');
        const x = parseFloat(values[0]);
        const y = parseFloat(values[1]);
        const z = parseFloat(values[2]);
        positions.push(x, y, z);
    }
    // Set the positions as an attribute of the geometry
    geometry.setAttribute('position', new THREE.Float32BufferAttribute(positions, 3));

    // Create spheres based on the positions
    const radius = 0.1; // Adjust the radius of the spheres as needed
    const sphereGeometry = new THREE.SphereGeometry(radius, 32, 32);
    const spheres = new THREE.Group();

    for (let i = 0; i < positions.length; i += 3) {
        const sphere = new THREE.Mesh(sphereGeometry, material);
        sphere.position.set(positions[i], positions[i + 1], positions[i + 2]);
        spheres.add(sphere);
    }
    // Add ambient light to the scene
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5); // Adjust the intensity as needed
    scene.add(ambientLight);

    // Add directional light to the scene
    const directionalLight = new THREE.DirectionalLight(0xffffff, 1); // Adjust the intensity as needed
    directionalLight.position.set(0, 1, 0); // Set the position of the light
    scene.add(directionalLight);
    // Add the spheres to the scene
    scene.add(spheres);
    sendSceneToServer(positions,directionalLight,ambientLight);
}
function sendSceneToServer(points,dLight,aLight) {
  const url = '/upload_points/';
  const data = { points: points, directional_light: {'color':dLight.color,'intensity': dLight.intensity}, ambient_light: {'color':aLight.color,'intensity': aLight.intensity} };

  fetch(url, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(data),
  })
  .then((response) => response.json())
  .then((data) => {
    // Handle the response from the server
    console.log(data);
  })
  .catch((error) => {
    // Handle any errors that occurred during the request
    console.error(error);
  });
}

