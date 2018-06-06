// Фиксация работы CSRF.
$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (settings.type == 'POST' || settings.type == 'PUT' || settings.type == 'DELETE') {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }
            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    }
});

// Автоматизация выпадающего меню.
$(function() {
  function onNavbar() {
    if (window.innerWidth >= 768) {
      $('.navbar-inverse .dropdown').on('mouseover', function(){
        $('.dropdown-toggle', this).next('.dropdown-menu').show();
      }).on('mouseout', function(){
        $('.dropdown-toggle', this).next('.dropdown-menu').hide();
      });
      $('.dropdown-toggle').click(function() {
        if ($(this).next('.dropdown-menu').is(':visible')) {
          window.location = $(this).attr('href');
        }
      });
    } else {
      $('.navbar-inverse .dropdown').off('mouseover').off('mouseout');
    }
  }
  $(window).resize(function() {
    onNavbar();
  });
  onNavbar();
});

// Фиксация работы required для нескольких check box.
$(function() {
    $('button[type="submit"]').on('click', function() {
        $('[class^=cbxcls-]').each(function() {
            let cbx_group = $(this).find("input");
            cbx_group.prop('required', true);
            if(cbx_group.is(":checked")){
                cbx_group.prop('required', false);
            };
        });
    });
});

// Очистка проверки при клике на check box.
function clearCheckBoxValidity(cls){
    let cbxs = document.getElementsByClassName('cbx-'+cls);
    for (let i=0; i < cbxs.length; i++) {
        cbxs[i].removeAttribute('required');
        cbxs[i].removeAttribute('oninvalid');
        cbxs[i].setCustomValidity('');
    }
}

// Очистка проверки при клике на radio button.
function clearRadioValidity(cls){
    let rads = document.getElementsByClassName('rad-'+cls);
    for (let i=0; i < rads.length; i++) {
        rads[i].removeAttribute('required');
        rads[i].removeAttribute('oninvalid');
        rads[i].setCustomValidity('');
    }
}

// Обработчик события submit на тестовой странице.
$(function() {
    $("#ajax_form").submit(
		function(){
            var arr = $('#ajax_form').serializeArray(), obj = {};
            $.each(arr, function(indx, el){
                  obj[el.name] ? obj[el.name].push(el.value) : (obj[el.name] = [el.value]);
            });
            $.ajax({
                url: window.location.pathname.split('/')[2] + '/' + "process_answer", //url страницы
                type: "POST", //метод отправки
                data: JSON.stringify(obj),  // Сеарилизуем объект
                success: function(response) { //Данные отправлены успешно
                    let content = $(response).find('.content');
                    $('.content').html(content);
                },
                error: function(response) { // Данные не отправлены
                    alert("Извините, возникла ошибка! Пожалуйста, попробуйте позже.");
                }
            });
			return false;
		}
    );
});
