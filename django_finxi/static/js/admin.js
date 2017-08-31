if (typeof jQuery === "undefined") {
    throw new Error("Carregar JQuery antes deste arquivo.");
}

$.Admin = {};

// topBar
$.Admin.topBar = {
    init: function (search_url) {
        var _this = this;

        _this.activateAutocompleteCategory();

        //Autocompletar busca
        $("input[name='endereco_imovel']").on('input', function(){
            if($(this).val()){
                var post_data = {
                    'enderecoBusca': $(this).val(),
                }
                _this.autocompleteBusca(search_url, post_data);
            }
        });

        //Prevenir busca vazia
        $('#search_form').submit(function() {
            if ($.trim($("input[name='endereco_imovel']").val()) === "") {
                return false;
            }
        });
    },

    autocompleteBusca: function(search_url, post_data) {
        var _this = this;
        post_data.csrfmiddlewaretoken = $.Admin.cookies.getCookie('csrftoken');
        $.ajax({
            type: "POST",
            url: search_url,
            data: post_data,
            dataType: "text",
            success: function(data){_this.processBuscaData(data);}
        });
    },

    processBuscaData: function(data) {
        var busca_input = $("input[name='endereco_imovel']");
        var enderecos_cadastrados = []
        obj = JSON.parse(data);
        for (var i = 0; i < obj['cidades'].length; i++) {
            enderecos_cadastrados.push({value:obj['cidades'][i], label:obj['cidades'][i], category: 'Cidades'});
        }
        for (var i = 0; i < obj['bairros'].length; i++) {
            enderecos_cadastrados.push({value:obj['bairros'][i], label:obj['bairros'][i], category: 'Bairros'});
        }
        for (var i = 0; i < obj['regioes'].length; i++) {
            enderecos_cadastrados.push({value:obj['regioes'][i], label:obj['regioes'][i], category: 'Regiões'});
        }
        busca_input.catcomplete({
            minLength:2,
            source: enderecos_cadastrados,
            messages: {
                noResults:'',
                results:function(){}
            }
        });
    },

    activateAutocompleteCategory: function() {
        $.widget( "custom.catcomplete", $.ui.autocomplete, {
             _create: function() {
                this._super();
                this.widget().menu( "option", "items", "> :not(.ui-autocomplete-category)" );
            },

             _resizeMenu: function() {
                 this.menu.element.outerWidth(470).outerHeight(300);
             },

             _renderMenu: function( ul, items ) {

                 var that = this,
                currentCategory = "";

                 $.each( items, function( index, item ) {
                    var li;
                    if ( item.category != currentCategory ) {
                        ul.append( "<li class='ui-autocomplete-category " + item.category + "'>" + item.category + "</li>" );
                        currentCategory = item.category;
                    }

                    li = that._renderItemData( ul, item );

                    if ( item.category ) {
                        li.attr( "aria-label", item.category + " : " + item.label );
                    }
                });
            },

             _renderItem: function( ul, item ) {
                return $( "<li>" )
                .addClass(item.category)
                .attr( "data-value", item.value )
                .append( $( "<a>" ).text( item.label ) )
                .appendTo( ul );
            }
        });
    }
}

//Lista Imoveis
$.Admin.ListaImoveis = {
    init: function() {
        var _this = this;
        $('.imovel-block').click(function() {
            window.location = $(this).attr("data-href");
            return false;
        });

        $('.delete_btn').click(function(){
            var obj_id = $(this).attr('id');
            $('#confirm_modal').modal('show');
            $('#confirm_modal').find('input').val(obj_id);
        });

        $('#confirmar_delete').click(function() {
            $('#modal_form').submit();
        });
    }
}

$.Admin.maskInput = {
    maskImovel: function() {
        $('.decimal-mask').mask('000.000.000.000,00', {reverse: true});
    },
}

$.Admin.cookies = {
    getCookie: function(cookieName){
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                if (cookie.substring(0, cookieName.length + 1) === (cookieName + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(cookieName.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    },
}
