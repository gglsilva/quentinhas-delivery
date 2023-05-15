var mensagem = function () {
    return document.getElementById('msg').value
}
var cliente = function () {
    var select = document.getElementById('select-client');
    var userSelect = select.options[select.selectedIndex].value;
    return userSelect
}

var recuperaCheckbox = function () {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    var quentinha = new Array()
    for (var checkbox of checkboxes) {
        quentinha.push(checkbox.value)
    }
    return quentinha
}
function desmarcaCheckbox() {
    var inputs = $('input[type=checkbox]');
    inputs.attr('checked', false);
    inputs.prop('checked', false);
}
function redirecionaCliente() {
    window.location = "{% url 'orders:order_created' %}"
}

function saveContent() {
    var checkboxes = document.querySelectorAll('input[type="checkbox"]:checked');
    var quentinha = new Array()
    for (var checkbox of checkboxes) {
        quentinha.push(checkbox.value)
    }
    $.ajax({
        type: "POST",
        url: "{% url 'orders:action_ajax_create_order' %}",
        data: {
            produtos: quentinha,
            cliente: '{{ user }}',
            msg: mensagem,
            csrfmiddlewaretoken: '{{ csrf_token }}',
        },
        success: function (data) {
            if (data['response'] == 'success') {
                console.log('Aqui')
                console.log(data['response'])
            }
            alert('Obrigado pelo seu pedido!')
        },
        error: function (error) {
            console.log('error: ' + error) //exibe na aba console do navegador
            //ou
            alert('error: ' + error) //exibe janela de texto
        },
        complete: function (jqXHR, textStatus) {
            desmarcaCheckbox()
            const msg = document.getElementById('msg').value = "";
            redirecionaCliente();
            // alert('Obrigado pelo seu pedido!')
        }
    })
}