/**
 * bet-sites.js
 * Datos base de reseñas para /bet.
 * Esquema mixto: campos obligatorios + opcionales.
 *
 * Obligatorios:
 * - id, name, type, summary, referralLink
 *
 * Opcionales usados:
 * - trustScore, bonus, terms, paymentMethods, pros, cons, tags, disclaimerNote
 */

window.betSitesData = [
  {
    "id": "test-casino-alpha",
    "name": "Test Casino Alpha",
    "type": "casino",
    "trustScore": 4,
    "summary": "Reseña de prueba para el hub de apuestas. Plataforma simple con pocos métodos de pago.",
    "bonus": "Bono de bienvenida del 100% hasta 200 USD",
    "terms": "Apuesta mínima 0.5 USD; rollover x35; retiro sujeto a verificación.",
    "paymentMethods": ["credit_card", "pix", "binance_pay"],
    "pros": ["Interfaz sencilla", "Pix disponible"],
    "cons": ["Catálogo reducido", "Soporte limitado"],
    "referralLink": "#",
    "tags": ["argentina", "latam", "test"],
    "disclaimerNote": "Registro de prueba. Verificar términos oficiales antes de usar."
  },
  {
    "id": "test-casino-beta",
    "name": "Test Casino Beta",
    "type": "casino",
    "trustScore": 2,
    "summary": "Reseña de prueba con alerta. Información incompleta y señales de riesgo para revisar.",
    "bonus": "Pack de bienvenida en 3 depósitos",
    "terms": "Términos poco claros; withholdings altos; retrasos reportados en retiros.",
    "paymentMethods": ["cripto"],
    "pros": ["Depósitos rápidos"],
    "cons": ["Retiros lentos", "Términos confusos", "Pocas reseñas confiables"],
    "referralLink": "#",
    "tags": ["worldwide", "scam-warning", "test"],
    "disclaimerNote": "Ejemplo con alerta de riesgo. No recomendado hasta verificación."
  },
  {
    "id": "test-casino-gamma",
    "name": "Test Casino Gamma",
    "type": "casino",
    "trustScore": 3,
    "summary": "Reseña de prueba intermedia. Algunos elementos positivos, pero requiere actualización de términos.",
    "bonus": "Bonos free spins en depósitos semanales",
    "terms": "Free spins válidos 72h; exclusivos para slots marcadas.",
    "paymentMethods": ["credit_card", "pix", "skrill", "neteller"],
    "pros": ["Variedad de pagos", "Promos recurrentes"],
    "cons": ["Rollover alto", "APP inestable"],
    "referralLink": "#",
    "tags": ["latam", "promo", "test"],
    "disclaimerNote": "Reseña de prueba. Revisar fecha de validez del bono."
  }
];
