function render({ model, el }) {
    // Make iframe 
    let iframe = document.createElement("iframe");
    iframe.src = "http://localhost:8080/";
    iframe.classList.add("my-frame")
    el.classList.add("widget-wrapper");

    el.appendChild(iframe);
}
export default { render };