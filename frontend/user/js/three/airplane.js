// ## 📄 **js/three/airplane.js**
// ```javascript

// // ================================================================
// // Three.js Airplane Animation
// // ================================================================

import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';

let scene, camera, renderer, airplane, cloud1, cloud2, cloud3;
let isActive = true;

export function initAirplane() {
    const canvas = document.getElementById('threeCanvas');
    if (!canvas) return;
    
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
    camera.position.z = 15;
    camera.position.y = 2;
    
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
    
    // Create airplane
    createAirplane();
    
    // Create clouds
    createClouds();
    
    // Animation
    animate();
    
    // Handle resize
    window.addEventListener('resize', onWindowResize);
    
    isActive = true;
}

function createAirplane() {
    const group = new THREE.Group();
    
    // Fuselage
    const fuselageGeometry = new THREE.CylinderGeometry(0.5, 0.5, 3, 8);
    const fuselageMaterial = new THREE.MeshPhongMaterial({ 
        color: 0xEB4304,
        emissive: 0xEB4304,
        emissiveIntensity: 0.2
    });
    const fuselage = new THREE.Mesh(fuselageGeometry, fuselageMaterial);
    fuselage.rotation.z = Math.PI / 2;
    group.add(fuselage);
    
    // Wings
    const wingGeometry = new THREE.BoxGeometry(6, 0.1, 1.5);
    const wingMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x236571,
        emissive: 0x236571,
        emissiveIntensity: 0.2
    });
    const wings = new THREE.Mesh(wingGeometry, wingMaterial);
    group.add(wings);
    
    // Tail
    const tailGeometry = new THREE.BoxGeometry(0.1, 1.5, 1);
    const tail = new THREE.Mesh(tailGeometry, wingMaterial);
    tail.position.x = -1.5;
    tail.position.y = 0.5;
    group.add(tail);
    
    airplane = group;
    airplane.position.x = -10;
    scene.add(airplane);
}

function createClouds() {
    const cloudGeometry = new THREE.SphereGeometry(1, 8, 8);
    const cloudMaterial = new THREE.MeshPhongMaterial({ 
        color: 0xffffff,
        transparent: true,
        opacity: 0.3
    });
    
    cloud1 = new THREE.Mesh(cloudGeometry, cloudMaterial);
    cloud1.position.set(-5, 3, -5);
    cloud1.scale.set(2, 1, 1);
    scene.add(cloud1);
    
    cloud2 = new THREE.Mesh(cloudGeometry, cloudMaterial);
    cloud2.position.set(5, -2, -8);
    cloud2.scale.set(1.5, 1, 1);
    scene.add(cloud2);
    
    cloud3 = new THREE.Mesh(cloudGeometry, cloudMaterial);
    cloud3.position.set(0, 4, -10);
    cloud3.scale.set(1.8, 0.8, 1);
    scene.add(cloud3);
}

function animate() {
    if (!isActive) return;
    
    requestAnimationFrame(animate);
    
    // Animate airplane
    if (airplane) {
        airplane.position.x += 0.03;
        airplane.position.y = Math.sin(Date.now() * 0.001) * 0.5;
        airplane.rotation.z = Math.sin(Date.now() * 0.001) * 0.1;
        
        if (airplane.position.x > 15) {
            airplane.position.x = -15;
        }
    }
    
    // Animate clouds
    if (cloud1) cloud1.position.x -= 0.01;
    if (cloud2) cloud2.position.x -= 0.015;
    if (cloud3) cloud3.position.x -= 0.008;
    
    if (cloud1 && cloud1.position.x < -15) cloud1.position.x = 15;
    if (cloud2 && cloud2.position.x < -15) cloud2.position.x = 15;
    if (cloud3 && cloud3.position.x < -15) cloud3.position.x = 15;
    
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

export function cleanupAirplane() {
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

// Auto-initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initAirplane);
} else {
    initAirplane();
}