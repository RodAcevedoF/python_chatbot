// Use relative URLs so the UI works on any domain (localhost, Render, etc.)
const API_URL = '/chat';
const HOTEL_INFO_URL = '/hotel-info';
const sessionId = `session-${Date.now()}-${Math.random()
	.toString(36)
	.substring(2, 9)}`;

const messagesDiv = document.getElementById('messages');
const input = document.getElementById('input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');

let isProcessing = false;
let hotelInfo = null;

window.addEventListener('DOMContentLoaded', () => {
	addMessage(
		'¡Bienvenido a Hotel Costa Azul! 👋\n\nSoy Costy, tu asistente virtual. Estaré encantado de ayudarte con cualquier duda sobre nuestro hotel, servicios, habitaciones y recomendaciones.\n\n¿En qué puedo ayudarte hoy?',
		'bot',
	);
	input.focus();
	loadHotelInfo();
});

function addMessage(text, sender) {
	const div = document.createElement('div');
	div.className = `message ${sender}`;
	div.innerText = text;
	messagesDiv.appendChild(div);
	scrollToBottom();
}

function scrollToBottom() {
	setTimeout(() => {
		messagesDiv.scrollTop = messagesDiv.scrollHeight;
	}, 100);
}

function showTypingIndicator() {
	typingIndicator.style.display = 'block';
	scrollToBottom();
}

function hideTypingIndicator() {
	typingIndicator.style.display = 'none';
}

function setProcessingState(processing) {
	isProcessing = processing;
	sendButton.disabled = processing;
	input.disabled = processing;

	if (processing) {
		sendButton.style.opacity = '0.6';
	} else {
		sendButton.style.opacity = '1';
		input.focus();
	}
}

async function sendMessage(text = null) {
	const message = text || input.value.trim();
	if (!message || isProcessing) return;

	addMessage(message, 'user');
	input.value = '';

	setProcessingState(true);
	showTypingIndicator();

	try {
		const res = await fetch(API_URL, {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({
				message,
				session_id: sessionId,
			}),
		});

		if (!res.ok) {
			throw new Error(`Error del servidor: ${res.status}`);
		}

		const data = await res.json();
		hideTypingIndicator();
		addMessage(data.reply, 'bot');
	} catch (error) {
		console.error('Error:', error);
		hideTypingIndicator();
		addMessage(
			'Lo siento, ha ocurrido un error. Por favor, intenta de nuevo o contacta con recepción.',
			'bot',
		);
	} finally {
		setProcessingState(false);
	}
}

function sendQuick(text) {
	if (!isProcessing) {
		sendMessage(text);
	}
}

input.addEventListener('keydown', (e) => {
	if (e.key === 'Enter' && !e.shiftKey) {
		e.preventDefault();
		sendMessage();
	}
});

input.addEventListener('keypress', (e) => {
	if (e.key === 'Enter' && !e.shiftKey) {
		e.preventDefault();
	}
});

// Hotel Info Functions
async function loadHotelInfo() {
	try {
		const res = await fetch(HOTEL_INFO_URL);
		if (res.ok) {
			hotelInfo = await res.json();
		}
	} catch (error) {
		console.error('Failed to load hotel info:', error);
	}
}

function toggleInfo() {
	const content = document.getElementById('info-content');
	const arrow = document.getElementById('info-arrow');
	const loading = document.getElementById('info-loading');
	const data = document.getElementById('info-data');

	if (content.classList.contains('open')) {
		content.classList.remove('open');
		arrow.classList.remove('open');
		content.style.display = 'none';
	} else {
		content.classList.add('open');
		arrow.classList.add('open');
		content.style.display = 'block';

		if (hotelInfo && data.innerHTML === '') {
			loading.style.display = 'none';
			data.style.display = 'block';
			renderHotelInfo();
		}
	}
}

function renderHotelInfo() {
	if (!hotelInfo) return;

	const data = document.getElementById('info-data');
	let html = '';

	if (hotelInfo.address) {
		html += `
			<div class="info-section">
				<div class="info-section-title">📍 Ubicación</div>
				<div class="info-section-content">
					${hotelInfo.address.street}, ${hotelInfo.address.city} ${hotelInfo.address.postal_code}
				</div>
			</div>
		`;
	}

	if (hotelInfo.rating) {
		const stars = '⭐'.repeat(Math.round(hotelInfo.rating.average));
		html += `
			<div class="info-section">
				<div class="info-section-title">⭐ Valoración</div>
				<div class="info-section-content">
					<div class="info-rating">
						<span class="info-stars">${stars}</span>
						<span>${hotelInfo.rating.average}/5</span>
					</div>
				</div>
			</div>
		`;
	}

	if (hotelInfo.hours) {
		html += `
			<div class="info-section">
				<div class="info-section-title">🕐 Horarios</div>
				<div class="info-section-content">
					<div class="info-item"><strong>Desayuno:</strong> ${hotelInfo.hours.breakfast}</div>
					<div class="info-item"><strong>Spa:</strong> ${hotelInfo.hours.spa}</div>
					<div class="info-item"><strong>Piscina:</strong> ${hotelInfo.hours.pool}</div>
				</div>
			</div>
		`;
	}

	if (hotelInfo.contact) {
		html += `
			<div class="info-section">
				<div class="info-section-title">📞 Contacto</div>
				<div class="info-section-content">
					<div class="info-item"><strong>Teléfono:</strong> ${hotelInfo.contact.phone}</div>
					<div class="info-item"><strong>Email:</strong> ${hotelInfo.contact.email}</div>
				</div>
			</div>
		`;
	}

	if (hotelInfo.faqs && hotelInfo.faqs.length > 0) {
		html += `
			<div class="info-section">
				<div class="info-section-title">❓ Preguntas Frecuentes</div>
				<div class="info-section-content">
		`;
		hotelInfo.faqs.forEach((faq) => {
			html += `
				<div class="info-faq">
					<div class="info-faq-q">${faq.q}</div>
					<div class="info-faq-a">${faq.a}</div>
				</div>
			`;
		});
		html += `
				</div>
			</div>
		`;
	}

	if (hotelInfo.policies) {
		html += `
			<div class="info-section">
				<div class="info-section-title">📋 Políticas</div>
				<div class="info-section-content">
					<div class="info-item"><strong>Cancelación:</strong> ${hotelInfo.policies.cancellation}</div>
					<div class="info-item"><strong>Depósito:</strong> ${hotelInfo.policies.deposit}</div>
				</div>
			</div>
		`;
	}

	data.innerHTML = html;
}
