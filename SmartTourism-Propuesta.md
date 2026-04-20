# 🗺️ **SmartTourism City Guide**
## *La revolución del turismo inteligente y humano*

---

## 🎯 **1. El Concepto**

### ✨ La Gran Idea

**SmartTourism City Guide** es más que una app de turismo. Es un **ecosistema vivo** que aprende, conecta y humaniza la experiencia de viajar.

> 💡 Combina información en tiempo real, IA adaptativa y conexiones humanas para crear viajes únicos y significativos en A Coruña.

---

### 🔴 El Problema Que Resolvemos

Las guías tradicionales son... **estáticas, solitarias, ciegas**:

| ❌ Antes | ✅ SmartTourism |
|----------|-----------------|
| No saben quién eres | 👤 Perfil inteligente que aprende |
| Ignoran aforos reales | 📊 Semáforo vivo de ocupación |
| Sin contexto en tiempo real | ⚡ Bandera roja en la playa, clima, alertas |
| Sin memoria | 🧠 Recuerdan tus intereses reales |
| Te aíslan | 🤝 Conectan viajeros afines |

**Resultado**: Tours genéricos, museos abarrotados, turistas solos perdidos en mapas.

**SmartTourism**: Experiencias personalizadas, viajeros conectados, datos que fluyen.

---

## 🧬 **2. Las 12 Entidades NGSI-LD** 
### *(El Corazón del Sistema)*

```
      ┌─────────────────────────────────┐
      │    GRAFO DE CONOCIMIENTO        │
      │   (Evoluciona Constantemente)    │
      └─────────────────────────────────┘
```

#### **👤 TouristProfile**
Quién eres: idioma, nacionalidad, intereses, movilidad, espíritu socializador.  
**Magia**: La IA descubre tus intereses reales por tu comportamiento.

---

#### **🎒 TouristTrip**
Tu itinerario vivo. Dónde estás, dónde fuiste, tu huella en la ciudad.  
**Timestamps reales**: Entrada y salida de cada POI.

---

#### **🏛️ TouristDestination**
A Coruña encapsulada: clima, idiomas, aforo máximo, capacidad.  
**Temporada + Pulso**: Qué está vivo ahora.

---

#### **📍 PointOfInterest (POI)**
Cualquier lugar: coordenadas, valoración, aforo dinámico.  
**Base de todo el mapa**.

---

#### **🎨 Museum**
La Torre de Hércules, MARCO, Museo de Bellas Artes.  
**Datos**: Aforo máximo, precios, colecciones, audioguías multiidioma, horarios.

---

#### **🏖️ Beach**
Playas de A Coruña.  
**Datos**: Longitud, bandera (🟢🟡🔴), temperatura del agua, calidad, servicios.

---

#### **🎪 Event**
Conciertos, ferias, rutas, festivales.  
**Dinámicos**: Aforo, precios, ubicación.

---

#### **🚲 TouristRental**
Bicis, patinetes, tours guiados.  
**Real-time**: Disponibilidad vía MQTT ⚡

---

#### **📊 ConsumptionBehavior**
Tu huella digital: cuánto tiempo pasaste, cuánto gastaste, dónde fuiste.  
**Combustible del ML**: Alimenta el aprendizaje continuo.

---

#### **💘 SocialMatch** *(LA NOVEDAD)*
**Matchmaking humano**: Cuando dos viajeros son afines.  
- Puntuación de afinidad (algorítmica)
- POI sugerido para el encuentro
- Estado de invitación: pendiente → aceptada → encuentro real

*Convierte extraños en compañeros de viaje.*

---

#### **🔔 Alert**
Notificaciones inteligentes:
- 📢 Aforo > 80%
- 🌊 Cambios de bandera en playas
- 📅 Cancelación de eventos
- 🌩️ Alertas climáticas
- 💬 Nuevas propuestas de encuentro

---

#### **📡 Device**
El hardware que ve la ciudad:
- 📷 Cámaras de conteo
- 📍 Beacons BLE
- 🌡️ Sensores meteorológicos
- 🏷️ Códigos QR/NFC para check-ins

---

## ⚙️ **3. Las 6 Funcionalidades Clave**

### **F1️⃣ – Mapa Inteligente de la Ciudad**
*Leaflet + OpenStreetMap*

```
🟢 Verde (disponible)
🟡 Amarillo (>70% aforo)
🔴 Rojo (lleno/cerrado)
```

✨ **Qué ves**:
- POIs, museos, playas, eventos con iconos bonitos
- Semáforo de ocupación en vivo
- Puntuación de afinidad personal al tocar marcador
- Actualización WebSocket < 10 segundos

---

### **F2️⃣ – Motor de Recomendación**
*scikit-learn + embeddings*

🧠 **Cómo funciona**:
1. Analiza tu perfil + comportamiento pasado
2. Calcula distancias (GeoPandas)
3. Cruza horarios, aforos, perfiles similares
4. **Ajuste dinámico**: Pasaste 3h en un museo arqueológico → ¡La Torre de Hércules es tu próxima sugerencia!

---

### **F3️⃣ – Dashboard de Gestión**
*Grafana + QuantumLeap* (para el Concello)

📈 **Lo que ven los gestores**:
- Mapas de calor: dónde fluyen los turistas
- Nacionalidades y tiempos de permanencia
- Puntos calientes de socialización
- Zonas saturadas → decisiones: "Hay que añadir un bus"

---

### **F4️⃣ – Ciudad 3D Viva**
*Three.js*

🏙️ **La magia**:
- Reconstrucción 3D de A Coruña (footprints de OSM)
- **Los edificios respiran**: Crecen y cambian color según ocupación
- Partículas animadas = turistas moviéndose en tiempo real
- Hipnotizante para presentaciones y análisis

---

### **F5️⃣ – Guía Conversacional IA**
*Ollama local + Llama 3*

💬 **Habla natural**:
- "¿Está lleno el Museo de Bellas Artes?"
- "¿Qué eventos hay cerca del puerto este finde?"
- "¿Dónde alquilo una bici?"

✨ **Multi-idioma automático** según tu perfil.

---

### **F6️⃣ – Social Travel Match**
*El corazón humano del sistema*

🤝 **Matchmaking + Icebreaker**:

1. **Afinidad algorítmica**: Analiza comportamiento común
   - "Ambos dediquen tiempo a arte contemporáneo"
   - "Rutas que se cruzan hoy a las 16:00"

2. **Micro-encuentros**: "María también quiere ir al Aquarium a las 16:00. ¿Juntos + descuento de grupo?"

3. **Icebreaker IA**: La IA sugiere temas de conversación basados en intereses comunes

---

## 🛠️ **4. El Stack Tecnológico**

| Tecnología | Misión | 
|------------|---------| 
| **Orion CB** (NGSI-LD) | Estado vivo: POIs, aforos, eventos, alertas y matches |
| **Agente IoT** (HTTP/MQTT) | Contadores de aforo, APIs de eventos reales |
| **QuantumLeap + TimescaleDB** | Historial: cómo se comportan los turistas |
| **FastAPI + Python** | API REST, orquestación, alertas |
| **scikit-learn + embeddings** | Recomendaciones colaborativas, clustering social |
| **GeoPandas + Pandas** | Rutas óptimas, flujos geoespaciales |
| **Leaflet + OSM** | Mapa interactivo bonito |
| **Grafana** | Dashboard para gestores municipales |
| **Three.js** | Visualización 3D de la ciudad |
| **PWA (Responsive)** | App del turista con Service Workers |
| **Ollama + Llama 3** | IA conversacional local |
| **QR / NFC** | Check-in físico = datos reales |
| **WebSockets** | Actualizaciones instantáneas |

---

## 🔄 **5. El Ciclo de Datos**
### *(Efecto 10/10 – La Retroalimentación que Funciona)*

```
┌─────────────────────────────────────────────────────────┐
│                  VIAJERO ENTRA A A CORUÑA               │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ 1️⃣  LLEGADA         │
          │ TouristProfile creado│
          │ (intereses, apertura)│
          └──────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ 2️⃣  PLANIFICACIÓN      │
          │ ML genera TouristTrip  │
          │ (ruta 1.0)           │
          └──────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ 3️⃣  ACCIÓN           │
          │ Visita POIs (QR/Beacon)│
          │ Datos reales recogidos │
          └──────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ 4️⃣  APRENDIZAJE      │
          │ ConsumptionBehavior  │
          │ Perfil actualizado   │
          └──────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ 5️⃣  CONEXIÓN        │
          │ SocialMatch detecta  │
          │ viajeros afines      │
          │ Propuestas enviadas  │
          └──────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ 6️⃣  OPTIMIZACIÓN    │
          │ Recos hiper-personalizadas│
          │ Dinámicas de grupo   │
          └──────────────────────┘
                     │
                     ▼
          ┌──────────────────────┐
          │ 7️⃣  GESTIÓN         │
          │ Datos → Concello     │
          │ Mejora oferta        │
          └──────────────────────┘
                     │
                     ▼
            ✨ EXPERIENCIA ÚNICA ✨
```

---

## 🎭 **Casos de Uso en A Coruña**

### 📍 Escenario 1: María, 28 años, arquitecta de Barcelona

1. **Llegada**: Le encanta arquitectura medieval y moderna
2. **Planificación**: SmartTourism le prepara: Torre de Hércules → MARCO → Paseo Marítimo
3. **Acción**: Pasa 90 min en cada lugar (los datos lo saben)
4. **Conexión**: El sistema detecta a **Carlos**, ingeniero de Madrid, mismos intereses, ruta que se cruza hoy a las 16:00 en MARCO
5. **Resultado**: María y Carlos van juntos, se llevan bien, comparten fotos, descuento de grupo en el café

---

### 🏖️ Escenario 2: Familia Chen, turismo familiar

1. **Perfil**: Padres + 2 niños, interés en playas seguras
2. **Alerts**: "Bandera verde en Orzán, agua a 17°C, área de juego habilitada"
3. **Ruta**: Playa → Aquarium Finisterrae (sugerencia IA) → Mercado de Abastos
4. **Social**: Encuentran a otra familia similar, juegan los niños en la playa juntos
5. **Gestión**: El Concello ve "picos de familias a las 15:00 en Orzán" → más socorristas

---

### 🌙 Escenario 3: Viajero solitario, turismo responsable

1. **Entrada**: Solo, abierto a conocer gente
2. **IA**: "3 personas con tus intereses están visitando hoy la Torre de Hércules"
3. **Icebreaker**: Conversación sugerida: "Ambos venís de Portugal, ¿qué os trae?"
4. **Encuentro**: Comparten experiencia, fotos, contactos
5. **Salida**: No fue solo. Se va feliz.

---

## 🚀 **Por Qué Funciona**

✅ **Ciclo completo**: Datos → Aprendizaje → Acción → Mejora  
✅ **Humano primero**: Conexiones reales, no algoritmos fríos  
✅ **Local**: Ollama (sin datos a cloud), privacidad real  
✅ **Tiempo real**: WebSockets, < 10s de actualización  
✅ **Sostenible**: Menos aglomeraciones, mejor distribución de turismo  
✅ **Inclusivo**: Multiidioma, accesibilidad, movilidad reducida  

---

## 🎯 **Métricas de Éxito**

| KPI | Meta |
|-----|------|
| **Enganche turistas** | 80% vuelven a usar en próxima visita |
| **Conexiones sociales** | 30% de viajeros solos hacen amigos |
| **Distribución de aforo** | Picos reducidos 40% (menos aglomeración) |
| **Satisfacción** | 4.7★ en reviews |
| **Descubrimientos** | 50% visitan POIs no planeados |

---

## ✨ **La Magia Final**

**SmartTourism City Guide** no es simplemente una app.  
Es un **puente entre datos, máquinas y emociones humanas**.

Transforma A Coruña en una ciudad que:
- 🧠 Piensa en sus turistas
- 👥 Los conecta entre sí
- 📊 Aprende de sus historias
- 🎨 Crea experiencias memorables

---

*Hecho con ❤️ para viajeros, desarrolladores y ciudades.*

**GitHub**: [pablorubal/SmartTourism-City-Guide](https://github.com/pablorubal/SmartTourism-City-Guide)
