import './style.css'

const app = document.querySelector('#app');
const apiKey = import.meta.env.VITE_JULES_API_KEY;

const isConfigured = apiKey && apiKey !== 'YOUR_API_KEY_HERE' && apiKey.length > 0;

app.innerHTML = `
  <div>
    <h1>Jules Integration</h1>
    <div class="card">
      <h2>
        <span class="status-indicator ${isConfigured ? 'status-valid' : 'status-invalid'}"></span>
        System Status
      </h2>
      <p>
        ${isConfigured
    ? 'Jules is active and connected. Developing at lightspeed.'
    : 'Jules is waiting for configuration.'}
      </p>
      ${!isConfigured ? `
        <div class="instructions">
          <p>Please configure your API key to proceed.</p>
          <p>Edit the <code>.env</code> file in the project root:</p>
          <p><code>VITE_JULES_API_KEY=your_key_here</code></p>
          <p>Then restart the dev server.</p>
        </div>
      ` : `
        <button id="test-connection" style="margin-top: 1em;">Test Connection</button>
      `}
    </div>
  </div>
`

if (isConfigured) {
  document.querySelector('#test-connection').addEventListener('click', () => {
    alert(`Connected with key: ${apiKey.substring(0, 4)}...`);
  });
}
