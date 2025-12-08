// ## 📄 **js/three/ship.js**
// ```javascript
// // ================================================================
// // Three.js Ship Animation
// // ================================================================

import * as THREE from 'https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js';

let scene, camera, renderer, ship, waves;
let isActive = false;

export function initShip() {
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
    camera.position.set(0, 5, 15);
    camera.lookAt(0, 0, 0);
    
    // Renderer
    renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.setClearColor(0x000000, 0);
    canvas.appendChild(renderer.domElement);
    
    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
    scene.add(ambientLight);
    
    const directionalLight = new THREE.DirectionalLight(0x236571, 1);
    directionalLight.position.set(5, 5, 5);
    scene.add(directionalLight);
    
    // Create ship
    createShip();
    
    // Create waves
    createWaves();
    
    // Animation
    isActive = true;
    animate();
    
    // Handle resize
    window.addEventListener('resize', onWindowResize);
}

function createShip() {
    const group = new THREE.Group();
    
    // Hull
    const hullGeometry = new THREE.BoxGeometry(4, 1.5, 2);
    const hullMaterial = new THREE.MeshPhongMaterial({ 
        color: 0xEB4304,
        emissive: 0xEB4304,
        emissiveIntensity: 0.2
    });
    const hull = new THREE.Mesh(hullGeometry, hullMaterial);
    group.add(hull);
    
    // Deck
    const deckGeometry = new THREE.BoxGeometry(3.5, 0.3, 1.8);
    const deckMaterial = new THREE.MeshPhongMaterial({ 
        color: 0x236571,
        emissive: 0x236571,
        emissiveIntensity: 0.2
    });
    const deck = new THREE.Mesh(deckGeometry, deckMaterial);
    deck.position.y = 1;
    group.add(deck);
    
    // Containers
    const containerGeometry = new THREE.BoxGeometry(1, 0.8, 0.8);
    const containerMaterial = new THREE.MeshPhongMaterial({ color: 0x2E2F34 });
    
    for (let i = 0; i < 3; i++) {
        const container = new THREE.Mesh(containerGeometry, containerMaterial);
        container.position.set(-1 + i * 1, 1.6, 0);
        group.add(container);
    }
    
    ship = group;
    ship.position.y = 0;
    scene.add(ship);
}

function createWaves() {
    const geometry = new THREE.PlaneGeometry(50, 50, 20, 20);
    const material = new THREE.MeshPhongMaterial({ 
        color: 0x236571,
        transparent: true,
        opacity: 0.6,
        side: THREE.DoubleSide
    });
    
    waves = new THREE.Mesh(geometry, material);
    waves.rotation.x = -Math.PI / 2;
    waves.position.y = -1;
    scene.add(waves);
}

function animate() {
    if (!isActive) return;
    
    requestAnimationFrame(animate);
    
    const time = Date.now() * 0.001;
    
    // Animate ship
    if (ship) {
        ship.position.y = Math.sin(time) * 0.3;
        ship.rotation.z = Math.sin(time * 0.5) * 0.05;
        ship.rotation.x = Math.sin(time * 0.7) * 0.03;
    }
    
    // Animate waves
    if (waves && waves.geometry.attributes.position) {
        const positions = waves.geometry.attributes.position.array;
        for (let i = 0; i < positions.length; i += 3) {
            const x = positions[i];
            const y = positions[i + 1];
            positions[i + 2] = Math.sin(x * 0.5 + time) * 0.3 + Math.cos(y * 0.5 + time) * 0.3;
        }
        waves.geometry.attributes.position.needsUpdate = true;
    }
    
    renderer.render(scene, camera);
}

function onWindowResize() {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
}

export function cleanupShip() {
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