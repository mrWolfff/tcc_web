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