document.addEventListener('DOMContentLoaded', function() {
    const surahList = document.getElementById('surah-list');
    const ayahContainer = document.getElementById('ayah-container');
    const backButton = document.getElementById('back-button');
    const surahTitle = document.getElementById('surah-title');
    const ayahList = document.getElementById('ayah-list');

    // Cargar lista de Surahs
    fetch('/surahs')
        .then(response => {
            if (!response.ok) {
                throw new Error('Error en la respuesta del servidor');
            }
            return response.json();
        })
        .then(data => {
            console.log('Datos de Surahs recibidos:', data);
            if (data.data && Array.isArray(data.data)) {
                const surahs = data.data;
                surahs.forEach(surah => {
                    const surahCard = document.createElement('div');
                    surahCard.className = 'surah-card';
                    surahCard.innerHTML = `
                        <h3>${surah.number}. ${surah.nameSpanish}</h3>
                        <p class="arabic-text">${surah.name}</p>
                    `;
                    surahCard.addEventListener('click', () => loadSurah(surah.number));
                    surahList.appendChild(surahCard);
                });
            } else {
                throw new Error('Formato de datos inválido');
            }
        })
        .catch(error => {
            console.error('Error al cargar Surahs:', error);
            surahList.innerHTML = '<div class="error">Error al cargar las Surahs. Por favor, recarga la página.</div>';
        });

    // Cargar Surah específica
    function loadSurah(surahNumber) {
        console.log('Cargando Surah número:', surahNumber);
        fetch(`/surah/${surahNumber}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Error en la respuesta del servidor');
                }
                return response.json();
            })
            .then(data => {
                console.log('Datos de Surah recibidos:', data);
                surahList.classList.add('hidden');
                ayahContainer.classList.remove('hidden');
                
                if (!data.arabic || !data.arabic.data || !data.spanish || !data.spanish.data) {
                    throw new Error('Datos incompletos recibidos del servidor');
                }

                const arabicSurah = data.arabic.data;
                const spanishEdition = data.spanish.data[0];

                surahTitle.textContent = `${arabicSurah.nameSpanish} - ${arabicSurah.name}`;
                ayahList.innerHTML = '';

                arabicSurah.ayahs.forEach((ayah, index) => {
                    const spanishAyah = spanishEdition.ayahs[index];
                    const ayahDiv = document.createElement('div');
                    ayahDiv.className = 'ayah-item';
                    
                    // Usar Abu Bakr Al-Shatri como recitador
                    const audioUrl = `https://cdn.islamic.network/quran/audio/128/ar.shaatree/${ayah.number}.mp3`;
                    
                    ayahDiv.innerHTML = `
                        <div class="ayah-number">${ayah.numberInSurah}</div>
                        <div class="arabic-text">${ayah.text}</div>
                        <div class="translation">${spanishAyah ? spanishAyah.text : 'Traducción no disponible'}</div>
                        <audio class="audio-player" controls preload="none">
                            <source src="${audioUrl}" type="audio/mpeg">
                            Tu navegador no soporta el elemento de audio.
                        </audio>
                    `;
                    ayahList.appendChild(ayahDiv);
                });
            })
            .catch(error => {
                console.error('Error al cargar Surah:', error);
                ayahList.innerHTML = '<div class="error">Error al cargar la Surah. Por favor, intenta nuevamente.</div>';
            });
    }

    // Volver a la lista de Surahs
    backButton.addEventListener('click', () => {
        ayahContainer.classList.add('hidden');
        surahList.classList.remove('hidden');
    });
});
