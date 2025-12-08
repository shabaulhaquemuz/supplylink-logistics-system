// js/3d-scene.js - REALISTIC Fast-Moving Big Truck

window.addEventListener('load', () => {
  const canvas = document.getElementById('canvas3d');
  if (!canvas) return;

  if (typeof THREE === 'undefined') {
    console.error('THREE.js not loaded!');
    return;
  }

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(75, canvas.offsetWidth / canvas.offsetHeight, 0.1, 1000);
  const renderer = new THREE.WebGLRenderer({ canvas, alpha: true, antialias: true });

  renderer.setSize(canvas.offsetWidth, canvas.offsetHeight);
  renderer.setPixelRatio(window.devicePixelRatio);
  renderer.shadowMap.enabled = true;

  // ============================================
  // CREATE ULTRA-REALISTIC BIG TRUCK
  // ============================================
  const truckGroup = new THREE.Group();

  // REALISTIC COLORS
  const truckOrange = 0xeb5e28;
  const darkGray = 0x2b2b2b;
  const lightGray = 0x4a4a4a;
  const metallic = 0x8b8b8b;

  // CABIN (More angular and realistic)
  const cabinWidth = 2.8;
  const cabinHeight = 3.2;
  const cabinDepth = 2.2;

  // Lower cabin base
  const lowerCabinGeo = new THREE.BoxGeometry(cabinWidth, cabinHeight - 0.8, cabinDepth);
  const cabinMat = new THREE.MeshPhongMaterial({ 
    color: truckOrange,
    shininess: 90,
    specular: 0x444444
  });
  const lowerCabin = new THREE.Mesh(lowerCabinGeo, cabinMat);
  lowerCabin.position.set(0, 1.2, 5.5);
  lowerCabin.castShadow = true;
  truckGroup.add(lowerCabin);

  // Upper cabin (sleeper compartment)
  const upperCabinGeo = new THREE.BoxGeometry(cabinWidth, 1, cabinDepth - 0.3);
  const upperCabin = new THREE.Mesh(upperCabinGeo, cabinMat);
  upperCabin.position.set(0, 2.6, 5.3);
  upperCabin.castShadow = true;
  truckGroup.add(upperCabin);

  // Windshield (angled, realistic)
  const windshieldGeo = new THREE.BoxGeometry(cabinWidth - 0.3, 1.8, 0.1);
  const windshieldMat = new THREE.MeshPhongMaterial({ 
    color: 0x0a0a0a,
    transparent: true,
    opacity: 0.7,
    shininess: 100
  });
  const windshield = new THREE.Mesh(windshieldGeo, windshieldMat);
  windshield.position.set(0, 2, 6.5);
  windshield.rotation.x = -0.15;
  truckGroup.add(windshield);

  // Front bumper (realistic chrome)
  const bumperGeo = new THREE.BoxGeometry(cabinWidth, 0.4, 0.3);
  const bumperMat = new THREE.MeshPhongMaterial({ 
    color: metallic,
    shininess: 120,
    specular: 0xffffff
  });
  const bumper = new THREE.Mesh(bumperGeo, bumperMat);
  bumper.position.set(0, 0.5, 6.8);
  truckGroup.add(bumper);

  // Grille (detailed)
  const grilleGeo = new THREE.BoxGeometry(cabinWidth - 0.6, 1.2, 0.15);
  const grilleMat = new THREE.MeshPhongMaterial({ 
    color: darkGray,
    shininess: 80
  });
  const grille = new THREE.Mesh(grilleGeo, grilleMat);
  grille.position.set(0, 1.2, 6.7);
  truckGroup.add(grille);

  // Grille bars (horizontal lines)
  for (let i = 0; i < 5; i++) {
    const barGeo = new THREE.BoxGeometry(cabinWidth - 0.8, 0.08, 0.05);
    const bar = new THREE.Mesh(barGeo, bumperMat);
    bar.position.set(0, 0.8 + (i * 0.18), 6.75);
    truckGroup.add(bar);
  }

  // Realistic headlights (LED style)
  const headlightGeo = new THREE.BoxGeometry(0.4, 0.25, 0.15);
  const headlightMat = new THREE.MeshPhongMaterial({ 
    color: 0xffffcc,
    emissive: 0xffff88,
    emissiveIntensity: 0.8,
    shininess: 100
  });
  
  const headlight1 = new THREE.Mesh(headlightGeo, headlightMat);
  headlight1.position.set(-1, 0.8, 6.75);
  truckGroup.add(headlight1);
  
  const headlight2 = new THREE.Mesh(headlightGeo, headlightMat);
  headlight2.position.set(1, 0.8, 6.75);
  truckGroup.add(headlight2);

  // CARGO CONTAINER (Realistic trailer)
  const containerWidth = 2.9;
  const containerHeight = 3.8;
  const containerDepth = 11;

  const containerGeo = new THREE.BoxGeometry(containerWidth, containerHeight, containerDepth);
  const containerMat = new THREE.MeshPhongMaterial({ 
    color: 0xd4590c,
    shininess: 50,
    specular: 0x222222
  });
  const container = new THREE.Mesh(containerGeo, containerMat);
  container.position.set(0, 1.9, -2.5);
  container.castShadow = true;
  truckGroup.add(container);

  // Container corrugation (realistic ribbed texture)
  for (let i = -5; i < 6; i += 0.6) {
    const ribGeo = new THREE.BoxGeometry(0.08, containerHeight, 0.08);
    const ribMat = new THREE.MeshPhongMaterial({ 
      color: 0xb84e0a,
      shininess: 40
    });
    const rib1 = new THREE.Mesh(ribGeo, ribMat);
    rib1.position.set(1.5, 1.9, i);
    truckGroup.add(rib1);
    
    const rib2 = new THREE.Mesh(ribGeo, ribMat);
    rib2.position.set(-1.5, 1.9, i);
    truckGroup.add(rib2);
  }

  // Back doors (realistic metal doors)
  const doorGeo = new THREE.BoxGeometry(containerWidth - 0.1, containerHeight - 0.4, 0.25);
  const doorMat = new THREE.MeshPhongMaterial({ 
    color: 0xa8450c,
    shininess: 60
  });
  const backDoor = new THREE.Mesh(doorGeo, doorMat);
  backDoor.position.set(0, 1.9, -8);
  truckGroup.add(backDoor);

  // Door locks and hinges
  const lockGeo = new THREE.BoxGeometry(0.15, 0.6, 0.15);
  const lockMat = new THREE.MeshPhongMaterial({ color: darkGray, shininess: 100 });
  
  [-0.8, 0.8].forEach(x => {
    const lock = new THREE.Mesh(lockGeo, lockMat);
    lock.position.set(x, 1.9, -8.15);
    truckGroup.add(lock);
  });

  // REALISTIC WHEELS (Detailed)
  const wheelRadius = 0.55;
  const wheelWidth = 0.45;
  const tireGeo = new THREE.CylinderGeometry(wheelRadius, wheelRadius, wheelWidth, 32);
  const tireMat = new THREE.MeshPhongMaterial({ 
    color: 0x1a1a1a,
    shininess: 20
  });
  
  const rimGeo = new THREE.CylinderGeometry(wheelRadius * 0.65, wheelRadius * 0.65, wheelWidth + 0.1, 32);
  const rimMat = new THREE.MeshPhongMaterial({ 
    color: metallic,
    shininess: 110,
    specular: 0xffffff
  });

  const wheels = [];
  const rims = [];

  // Front wheels
  const frontWheelPositions = [
    [-1.6, 0.55, 4.5],
    [1.6, 0.55, 4.5]
  ];

  frontWheelPositions.forEach(pos => {
    const tire = new THREE.Mesh(tireGeo, tireMat);
    tire.rotation.z = Math.PI / 2;
    tire.position.set(...pos);
    tire.castShadow = true;
    truckGroup.add(tire);
    wheels.push(tire);
    
    const rim = new THREE.Mesh(rimGeo, rimMat);
    rim.rotation.z = Math.PI / 2;
    rim.position.set(...pos);
    truckGroup.add(rim);
    rims.push(rim);
  });

  // Back wheels (dual rear wheels for realism)
  const backWheelPositions = [
    [-1.6, 0.55, -1.5],
    [1.6, 0.55, -1.5],
    [-1.6, 0.55, -3.5],
    [1.6, 0.55, -3.5],
    [-1.6, 0.55, -5.5],
    [1.6, 0.55, -5.5]
  ];

  backWheelPositions.forEach(pos => {
    const tire = new THREE.Mesh(tireGeo, tireMat);
    tire.rotation.z = Math.PI / 2;
    tire.position.set(...pos);
    tire.castShadow = true;
    truckGroup.add(tire);
    wheels.push(tire);
    
    const rim = new THREE.Mesh(rimGeo, rimMat);
    rim.rotation.z = Math.PI / 2;
    rim.position.set(...pos);
    truckGroup.add(rim);
    rims.push(rim);
  });

  // Exhaust pipes (vertical, realistic)
  const exhaustGeo = new THREE.CylinderGeometry(0.12, 0.12, 3, 16);
  const exhaustMat = new THREE.MeshPhongMaterial({ 
    color: 0x333333,
    shininess: 90
  });
  
  [-1.4, 1.4].forEach(x => {
    const exhaust = new THREE.Mesh(exhaustGeo, exhaustMat);
    exhaust.position.set(x, 2.5, 4.2);
    truckGroup.add(exhaust);
  });

  // Side mirrors (realistic)
  const mirrorGeo = new THREE.BoxGeometry(0.4, 0.3, 0.5);
  const mirrorMat = new THREE.MeshPhongMaterial({ 
    color: darkGray,
    shininess: 100
  });
  
  [-1.7, 1.7].forEach(x => {
    const mirror = new THREE.Mesh(mirrorGeo, mirrorMat);
    mirror.position.set(x, 2.8, 5.5);
    truckGroup.add(mirror);
  });

  // Chassis connection (realistic fifth wheel)
  const fifthWheelGeo = new THREE.CylinderGeometry(0.5, 0.5, 0.3, 16);
  const fifthWheelMat = new THREE.MeshPhongMaterial({ color: darkGray });
  const fifthWheel = new THREE.Mesh(fifthWheelGeo, fifthWheelMat);
  fifthWheel.rotation.x = Math.PI / 2;
  fifthWheel.position.set(0, 1.2, 3.5);
  truckGroup.add(fifthWheel);

  scene.add(truckGroup);
  truckGroup.rotation.y = Math.PI; // FACE FORWARD

  // ============================================
  // ROAD
  // ============================================
  const roadGeometry = new THREE.PlaneGeometry(30, 100);
  const roadMaterial = new THREE.MeshPhongMaterial({ 
    color: 0x1a2744,
    side: THREE.DoubleSide
  });
  const road = new THREE.Mesh(roadGeometry, roadMaterial);
  road.rotation.x = -Math.PI / 2;
  road.position.y = -0.05;
  road.receiveShadow = true;
  scene.add(road);

  // Road lines (faster moving)
  const roadLines = [];
  for (let i = -40; i < 40; i += 6) {
    const lineGeometry = new THREE.BoxGeometry(0.35, 0.08, 3.5);
    const lineMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
    const line = new THREE.Mesh(lineGeometry, lineMaterial);
    line.position.set(0, 0.05, i);
    scene.add(line);
    roadLines.push(line);
  }

  // ============================================
  // BUILDINGS
  // ============================================
  for (let i = 0; i < 25; i++) {
    const x = (Math.random() - 0.5) * 50;
    const z = (Math.random() - 0.5) * 80;
    const height = Math.random() * 15 + 5;
    
    if (Math.abs(x) > 6) {
      const buildGeo = new THREE.BoxGeometry(4, height, 4);
      const buildMat = new THREE.MeshPhongMaterial({ 
        color: Math.random() > 0.5 ? 0x2d3748 : 0x1e293b,
        transparent: true,
        opacity: 0.75,
        shininess: 30
      });
      const building = new THREE.Mesh(buildGeo, buildMat);
      building.position.set(x, height / 2, z);
      building.castShadow = true;
      scene.add(building);
    }
  }

  // ============================================
  // LIGHTING (More realistic)
  // ============================================
  const ambientLight = new THREE.AmbientLight(0x404040, 1.5);
  scene.add(ambientLight);

  const directionalLight = new THREE.DirectionalLight(0xffffff, 1.8);
  directionalLight.position.set(15, 20, 15);
  directionalLight.castShadow = true;
  scene.add(directionalLight);

  const pointLight = new THREE.PointLight(0xff6b35, 2.5, 70);
  pointLight.position.set(0, 10, 10);
  scene.add(pointLight);

  const frontLight = new THREE.SpotLight(0xffffaa, 2);
  frontLight.position.set(0, 5, 15);
  frontLight.angle = Math.PI / 8;
  scene.add(frontLight);

  // Camera
  camera.position.set(10, 5, 14);
  camera.lookAt(0, 1.5, 0);

  // ============================================
  // ANIMATION (FASTER SPEED)
  // ============================================
  let truckRotation = 0;

  function animate() {
    requestAnimationFrame(animate);

    // FASTER road movement (was 0.15, now 0.35)
    roadLines.forEach(line => {
      line.position.z += 0.35;
      if (line.position.z > 50) {
        line.position.z = -50;
      }
    });

    // FASTER wheel rotation (was 0.12, now 0.25)
    wheels.forEach(wheel => {
      wheel.rotation.x += 0.25;
    });
    
    rims.forEach(rim => {
      rim.rotation.x += 0.25;
    });

    // Realistic suspension
    truckGroup.position.y = Math.sin(Date.now() * 0.003) * 0.06;
    truckGroup.rotation.z = Math.sin(Date.now() * 0.0015) * 0.01;

    // Dynamic camera
    truckRotation += 0.001;
    camera.position.x = Math.sin(truckRotation) * 13;
    camera.position.z = Math.cos(truckRotation) * 13 + 4;
    camera.position.y = 5 + Math.sin(truckRotation * 0.6) * 2;
    camera.lookAt(0, 1.5, 0);

    renderer.render(scene, camera);
  }

  animate();

  // ============================================
  // RESIZE
  // ============================================
  window.addEventListener('resize', () => {
    camera.aspect = canvas.offsetWidth / canvas.offsetHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(canvas.offsetWidth, canvas.offsetHeight);
  });

  // Counters
  function animateCounter(id, target, suffix = '') {
    let current = 0;
    const element = document.getElementById(id);
    if (!element) return;
    const increment = target / 50;
    const timer = setInterval(() => {
      current += increment;
      if (current >= target) {
        current = target;
        clearInterval(timer);
      }
      element.textContent = Math.floor(current) + suffix;
    }, 30);
  }

  setTimeout(() => {
    animateCounter('deliveriesCount', 1247);
    animateCounter('routesCount', 89);
    animateCounter('efficiencyCount', 98, '%');
  }, 1000);

  // Particles
  const hero = document.querySelector('.login-hero');
  if (hero) {
    for (let i = 0; i < 20; i++) {
      const particle = document.createElement('div');
      particle.className = 'particle';
      particle.style.left = Math.random() * 100 + '%';
      particle.style.top = Math.random() * 100 + '%';
      particle.style.animationDelay = Math.random() * 5 + 's';
      hero.appendChild(particle);
    }
  }

  console.log('✅ Realistic fast-moving truck loaded!');
});