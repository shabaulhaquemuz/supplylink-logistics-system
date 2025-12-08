// ## 📄 **js/three/truck.js**
// ```javascript
// // ================================================================
// // Three.js Truck Animation
// // ================================================================

import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';

let scene, camera, renderer, truck, road;
let isActive = false;

export function initTruck() {
    const canvas = document.getElementById('threeCanvas');
    if (!canvas) return;
    
    // Clear existing content
    canvas.innerHTML = '';
    
    // Scene
    scene = new THREE.Scene();
    scene.fog = new THREE.Fog(0x0a0a0a, 10, 50);
    
    // Camera
    camera = new THREE.PerspectiveCamera(
        75,
        window.innerWidth / window.innerHeight,
        0.1,
        1000
    );
    camera.position.set(5, 5, 12);
    camera.lookAt(0, 0, 0);
    
    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x000000, 0);
    canvas.appendChild(renderer.domElement);
    
    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0xEB4304, 1);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);
    
    // Create truck
    createTruck();
    
    // Create road
    createRoad();
    
    // Animation
    isActive = true;
    animate();
    
    // Handle resize
    window.addEventListener('resize', onWindowResize);
}

function createTruck() {
    const group = new THREE.Group();
    
    // Cabin
    const cabinGeometry = new THREE.BoxGeometry(2, 2, 2);
    const cabinMaterial = new THREE.MeshPhongMaterial({ 
        color: 0xEB4304,
        emissive: 0xEB4304,
        emissiveIntensity: 0.2
    });
    const cabin = new THREE.Mesh(cabinGeometry, cabinMaterial);
    cabin.position.set(-2, 1, 0);
    group.add(cabin);
    
    // Container
    const containerGeometry = new THREE.BoxGeometry(4, 2.5, 2);
    const containerMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x236571,
        emissive: 0x236571,
        emissiveIntensity: 0.2
    });
    const container = new THREE.Mesh(containerGeometry, containerMaterial);
    container.position.set(1, 1.25, 0);
    group.add(container);
    
    // Wheels
    const wheelGeometry = new THREE.CylinderGeometry(0.5, 0.5, 0.3, 16);
    const wheelMaterial = new THREE.MeshPhongMaterial({ color: 0x2E2F34 });
    
    const wheelPositions = [
        [-2.5, -0.5, 1],
        [-2.5, -0.5, -1],
        [2, -0.5, 1],
        [2, -0.5, -1],
    ];
    
    wheelPositions.forEach(pos => {
        const wheel = new THREE.Mesh(wheelGeometry, wheelMaterial);
        wheel.rotation.z = Math.PI / 2;
        wheel.position.set(...pos);
        group.add(wheel);
    });
    
    truck = group;
    truck.position.x = -10;
    scene.add(truck);
}

function createRoad() {
    const geometry = new THREE.PlaneGeometry(100, 5);
    const material = new THREE.MeshPhongMaterial({ 
        color: 0x2E2F34,
        side: THREE.DoubleSide
    });
    
    road = new THREE.Mesh(geometry, material);
    road.rotation.x = -Math.PI / 2;
    road.position.y = -1;
    scene.add(road);
    
    // Road markings
    const markingGeometry = new THREE.PlaneGeometry(2, 0.2);
    const markingMaterial = new THREE.MeshPhongMaterial({ color: 0xffffff });
    
    for (let i = -10; i < 10; i++) {
        const marking = new THREE.Mesh(markingGeometry, markingMaterial);
        marking.rotation.x = -Math.PI / 2;
        marking.position.set(i * 5, -0.99, 0);
        scene.add(marking);
    }
}

function animate() {
    if (!isActive) return;
    
    requestAnimationFrame(animate);
    
    // Animate truck
    if (truck) {
        truck.position.x += 0.05;
        
        // Small bounce
        truck.position.y = Math.sin(Date.now() * 0.01) * 0.05;
        
        if (truck.position.x > 15) {
            truck.position.x = -15;
        }
    }
    
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

export function cleanupTruck() {
    isActive = false;
    if (renderer) {
        const canvas = document.getElementById('threeCanvas');
        if (canvas && renderer.domElement) {
            canvas.removeChild(renderer.domElement);
        }
        renderer.dispose();
    }
    window.removeEventListener('resize', onWindowResize);
}