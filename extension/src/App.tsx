import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

function App() {
  const onclick = async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
      target: { tabId: tab.id! },
      func: () => {
        document.body.style.backgroundColor = "red";
      },
    });
  };

  const openModal = async () => {
    let [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
    chrome.scripting.executeScript({
      target: { tabId: tab.id! },
      func: () => {
        const modal = document.createElement("div");
        console.log(modal);
        modal.className = "modal";
        modal.innerHTML = `
                        <div class="modal-content" style="
                          background-color: #fefefe;
                          color: #000;
                          margin: 15% auto;
                          padding: 20px;
                          border: 1px solid #888;
                          width: 80%;
                        ">
                          <span class="close" style="
                          color: #aaa;
                          float: right;
                          font-size: 28px;
                          font-weight: bold
                          ">&times;</span>
                          <p>This is the modal content.</p>
                        </div>
                      `;
        document.body.appendChild(modal);
        modal.style.display = "block";
        modal.style.position = "fixed";
        modal.style.zIndex = "99";
        modal.style.left = "0";
        modal.style.top = "0";
        modal.style.width = "100%";
        modal.style.height = "100%";
        modal.style.overflow = "auto";
        modal.style.backgroundColor = "rgb(0,0,0, 0.8)";
        const closeButton = modal.querySelector('.close');
        if (closeButton) {
          closeButton.addEventListener('click', function() {
            modal.style.display = 'none';
          });
        }
      },
    });
  };

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={onclick}>Click Here!</button>
        <button onClick={openModal}>open modal</button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;
