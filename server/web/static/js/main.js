document.addEventListener("load", function () {
    function registerPaginationFormController() {
        const form = document.querySelector("[data-controller=pagination-form");
        if (!form) {
            return;
        }
        const select = form.querySelector("[data-pagination-form-target=select]");
        if (!select) {
            return;
        }
        select.addEventListener("change", () => form.dispatchEvent("change"));
    }
    
    registerPaginationFormController();
});

customElements.define('f-demo', class extends HTMLElement {
    connectedCallback() {
        console.log('hello');
    }
})
