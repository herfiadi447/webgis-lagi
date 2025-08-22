// Data layer dan legend
const layerData = {
    'Batuan Permukaan': {
        name: 'Batuan Permukaan',
        legend: [
            { color: '#3e19d2', label: 'S1 - Sangat Sesuai' },
            { color: '#6470f6', label: 'S2 - Sesuai' },
            { color: '#90d9f9', label: 'S3 - Cukup Sesuai' },
            { color: '#ff3c00', label: 'N - Tidak Sesuai' }
        ],
        description: 'Jenis batuan yang dominan di permukaan',
        info: '<h3>Batuan Permukaan</h3><p>Karakteristik batuan dominan di wilayah ini:</p><ul><li>Komposisi mineral</li><li>Tingkat pelapukan</li><li>Kedalaman lapisan</li></ul>'
    },
    // ...layer lain sesuai kebutuhan...
};

// Fungsi untuk mengontrol layer
function initLayerControls() {
    const layerTabs = document.querySelectorAll('.layer-tab');
    const supportInfoContainer = document.getElementById('support-info-container');
    const layerInfo = document.getElementById('layer-info');
    const mapLegend = document.getElementById('map-legend');
    const legendContent = document.getElementById('legend-content');

    // Fungsi untuk menampilkan iframe peta sesuai layer
    function showMapIframe(layer) {
        // Sembunyikan semua iframe
        document.querySelectorAll('.folium-map-tab').forEach(div => div.style.display = 'none');
        // Tampilkan iframe sesuai layer
        if (layer === 'none') {
            document.getElementById('folium-map-none').style.display = 'block';
        } else if (layer === 'Batuan Permukaan') {
            document.getElementById('folium-map-batuan').style.display = 'block';
        } else if (layer === 'KTK 2') {
            document.getElementById('folium-map-ktk').style.display = 'block';
        } else if (layer === 'C Organik') {
            document.getElementById('folium-map-corg').style.display = 'block';
        } else if (layer === 'pH') {
            document.getElementById('folium-map-ph').style.display = 'block';
        } else if (layer === 'Tesktur') {
            document.getElementById('folium-map-tekstur').style.display = 'block';
        } else if (layer === 'Drainase') {
            document.getElementById('folium-map-drainase').style.display = 'block';
        } else if (layer === 'Salinitas') {
            document.getElementById('folium-map-salinitas').style.display = 'block';
        } else if (layer === 'Kedalaman Tanah') {
            document.getElementById('folium-map-KedalamanTanah').style.display = 'block';
        } else if (layer === 'Kemiringan Lereng') {
            document.getElementById('folium-map-lereng').style.display = 'block';
        }
    }

    layerTabs.forEach(tab => {
        tab.addEventListener('click', function() {
            // Update UI tabs
            layerTabs.forEach(t => t.classList.remove('active'));
            this.classList.add('active');

            const layer = this.dataset.layer;

            // Sembunyikan legend dan info
            mapLegend.style.display = 'none';
            supportInfoContainer.style.display = 'none';

            // Tampilkan layer yang dipilih
            if (layer === 'none') {
                layerInfo.innerHTML = `<p>Pilih layer untuk melihat informasi lahan</p>`;
            } else {
                // Tampilkan informasi layer
                const currentLayer = layerData[layer];
                layerInfo.innerHTML = `
                    <h4>${currentLayer.name}</h4>
                    <p>${currentLayer.description}</p>
                `;

                // Buat legend
                legendContent.innerHTML = '';
                currentLayer.legend.forEach(item => {
                    legendContent.innerHTML += `
                        <div class="legend-item">
                            <div class="legend-color" style="background-color:${item.color}"></div>
                            <span>${item.label}</span>
                        </div>
                    `;
                });

                // Tampilkan info tambahan
                supportInfoContainer.style.display = 'block';
                supportInfoContainer.innerHTML = currentLayer.info;
                mapLegend.style.display = 'block';
            }

            // Tampilkan iframe peta sesuai layer
            showMapIframe(layer);
        });
    });

    // Add button functionality
    const addButton = document.getElementById('add-data');
    addButton.addEventListener('click', function() {
        alert('Fitur tambah data akan membuka form input data baru.');
    });

    // Aktifkan tab pertama (Tidak ada)
    document.querySelector('.layer-tab.active').click();
}

// Fungsi untuk menyembunyikan semua layer Folium
window.hideAllFoliumLayers = function() {
    if (!window.folium_map) return;
    window.folium_map.eachLayer(function(layer) {
        if (layer.options && layer.options.name && layer instanceof L.GeoJSON) {
            window.folium_map.removeLayer(layer);
        }
    });
};

// Fungsi untuk menampilkan layer Folium tertentu
window.showFoliumLayer = function(layerName) {
    if (!window.folium_map) return;
    window.hideAllFoliumLayers();
    window.folium_map.eachLayer(function(layer) {
        if (layer.options && layer.options.name === layerName && layer instanceof L.GeoJSON) {
            window.folium_map.addLayer(layer);
        }
    });
};

// Inisialisasi window.folium_map setelah peta Folium ter-load
setTimeout(function() {
    var mapDiv = document.querySelector('#folium-map > div');
    if (mapDiv && mapDiv.id) {
        window.folium_map = window[mapDiv.id];
    }
}, 500);

// Panggil initLayerControls saat halaman siap
document.addEventListener('DOMContentLoaded', function() {
    initLayerControls();
});

// Chatbot Groq via backend Flask (khusus dashboard)
document.addEventListener('DOMContentLoaded', function() {
    const chatbotMessages = document.getElementById('geoai-chatbot-messages');
    const chatbotForm = document.getElementById('geoai-chatbot-form');
    const chatbotInput = document.getElementById('geoai-chatbot-input');
    const chatbotSendBtn = document.getElementById('geoai-chatbot-send-btn');
    let chatbotConversation = [];

    function addChatbotMessage(text, sender) {
        const msgDiv = document.createElement('div');
        msgDiv.className = 'geoai-chatbot-message ' + sender;
        const bubble = document.createElement('div');
        bubble.className = 'geoai-chatbot-bubble';
        bubble.textContent = text;
        msgDiv.appendChild(bubble);
        chatbotMessages.appendChild(msgDiv);
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    }

    // Pesan sambutan otomatis
    if (chatbotMessages.childElementCount === 0) {
        addChatbotMessage("Halo! Saya GeoAI, asisten AI yang siap membantu Anda dengan berbagai informasi dan pertanyaan. Ada yang ingin Anda bicarakan atau tanyakan?", 'bot');
    }

    if (chatbotForm) {
        chatbotForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            const userMsg = chatbotInput.value.trim();
            if (!userMsg) return;
            addChatbotMessage(userMsg, 'user');
            chatbotInput.value = '';
            chatbotSendBtn.disabled = true;

            // Tampilkan loading
            const loadingMsg = document.createElement('div');
            loadingMsg.className = 'geoai-chatbot-message bot';
            loadingMsg.id = 'geoai-chatbot-loading-msg';
            loadingMsg.innerHTML = '<div class="geoai-chatbot-bubble">...</div>';
            chatbotMessages.appendChild(loadingMsg);
            chatbotMessages.scrollTop = chatbotMessages.scrollHeight;

            try {
                const response = await fetch('/chatbot', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: userMsg, conversation: chatbotConversation})
                });
                const data = await response.json();
                document.getElementById('geoai-chatbot-loading-msg').remove();
                let botMsg = data.reply || "Maaf, terjadi kesalahan.";
                chatbotConversation = data.conversation || [];
                addChatbotMessage(botMsg, 'bot');
            } catch (err) {
                document.getElementById('geoai-chatbot-loading-msg').remove();
                addChatbotMessage("Maaf, tidak dapat terhubung ke server.", 'bot');
            }
            chatbotSendBtn.disabled = false;
        });
    }
});