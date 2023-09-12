import Alpine from "alpinejs";

function TestApp() {
    return {
        init() {
            console.log('test app ready');
        },
        handleClick(e) {
            alert('eqsdqsdqsd');
        }
    }
}

Alpine.data("TestApp", TestApp)
