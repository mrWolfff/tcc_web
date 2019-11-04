document.addEventListener('DOMContentLoaded', function() {
    var elems = document.querySelectorAll('.dropdown-trigger');
    var instances = M.Dropdown.init(elems, options);
  });

  // Or with jQuery

  $('.dropdown-trigger').dropdown();

  $('#delete').on('click', function () {
    if(confirm("Deseja excluir a proposta? ")){
        window.location.href = "{% url 'deletePropostas' propostas.id   %}";
    }else{
        location.reload();
    }
});


document.addEventListener('DOMContentLoaded', function () {
    var elems = document.querySelectorAll('.modal');
    var instances = M.Modal.init(elems, options);
});
$(document).ready(function () {
    $('.modal').modal();
});
$('#edit').click(function () {
    confirm("");
    window.location.href = "#modal";
});
function Avaliar(estrela) {
    let cont;
    switch (estrela) {
        case 1:
            if ($('#star1').attr("src") == 'https://image.flaticon.com/icons/svg/148/148841.svg') {
                $('#star1').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                $('#star2').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                $('#star3').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                $('#star4').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                $('#star5').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                cont = 0;
                $('#rating').text(cont);
            } else {
                $('#star1').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                cont = 1;
                $('#rating').text(cont);
            }
            break;
        case 2:
            if ($('#star2').attr("src") == 'https://image.flaticon.com/icons/svg/148/148841.svg') {
                $('#star2').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                $('#star3').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                $('#star4').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                $('#star5').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                cont = 1;
                $('#rating').text(cont);
            } else {
                $('#star1').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                $('#star2').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                cont = 2;
                $('#rating').text(cont);
            }
            break;
        case 3:
            if ($('#star3').attr("src") == 'https://image.flaticon.com/icons/svg/148/148841.svg') {
                $('#star3').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                $('#star4').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                $('#star5').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                cont = 2;
                $('#rating').text(cont);
            } else {
                $('#star1').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                $('#star2').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                $('#star3').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                cont = 3;
                $('#rating').text(cont);
            }
            break;
        case 4:
            if ($('#star4').attr("src") == 'https://image.flaticon.com/icons/svg/148/148841.svg') {
                $('#star4').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                $('#star5').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                cont = 3;
                $('#rating').text(cont);
            } else {
                $('#star1').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                $('#star2').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                $('#star3').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                $('#star4').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                cont = 4;
                $('#rating').text(cont);
            }

            break;
        case 5:
            if ($('#star5').attr("src") == 'https://image.flaticon.com/icons/svg/148/148841.svg') {
                $('#star5').attr("src", "https://image.flaticon.com/icons/svg/149/149222.svg");
                cont = 4;
                $('#rating').text(cont);
            } else {
                $('#star1').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                $('#star2').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                $('#star3').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                $('#star4').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                $('#star5').attr("src", "https://image.flaticon.com/icons/svg/148/148841.svg");
                cont = 5;
                $('#rating').text(cont);
                console.log(cont);
            }
            break;
        default:
            console.log("Erro");

    }

}
$('#new_demanda').click(function () {
    window.location.href = "{% url 'cadastro_demanda' %}"
});