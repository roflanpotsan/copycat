(() => {
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i++) {
                    const cookie = cookies[i].trim();

                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        function rate(field, model, id, type=null){
            $.ajaxSetup({
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
                }
            });
            $.post( "/rate/", { model: model, id: id, type: type}).done(function( data ) {
                if ('new_rating' in data){
                    field.innerText = data['new_rating'];
                }
                else{
                    console.log(JSON.stringify(data));
                }
            });
        }
        function mark_correct(field, id){
            $.ajaxSetup({
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
                }
            });
            $.post( "/correct/", { id: id}).done(function( data ) {
                let tick = document.getElementsByClassName("tick")[0];
                if (tick != null){
                    let prev_field = tick.parentNode;
                    console.log(prev_field);
                    var btn = document.createElement("button");
                    let classes = ['btn', 'btn-outline-secondary', 'mb-3', 'mark-correct']
                    btn.classList.add(...classes);
                    btn.innerText = "Mark correct.";
                    let param = prev_field.parentNode.parentNode.id.split('_')[1];
                    console.log("PARAM", param);
                    btn.addEventListener("click", () => mark_correct(prev_field, param));
                    prev_field.innerHTML = '';
                    prev_field.appendChild(btn);
                }
                if ('success' in data){
                    var img = document.createElement("img");
                    img.src = "/static/img/tick.png";
                    img.classList.add('tick')
                    console.log(field.childNodes);
                    field.innerHTML = '';
                    field.appendChild(img);
                }
                else{
                    console.log(JSON.stringify(data));
                }
            });
        }
        window.onload = (event) => {
            rate_ups = document.querySelectorAll("button.rate-up");
            rate_downs = document.querySelectorAll("button.rate-down");

            console.log("LOADED");
            for (let i = 0; i < rate_ups.length; i++) {
                let params = rate_ups[i].parentNode.parentNode.parentNode.parentNode.id.split('_');
                let field = rate_ups[i].parentNode.parentNode.nextSibling.nextSibling.childNodes[1];
                rate_ups[i].addEventListener("click", () => {rate(field, params[0], params[1], 1)});
                rate_downs[i].addEventListener("click", () => {rate(field, params[0], params[1])});
            }

            correct_btn = document.querySelectorAll("button.mark-correct");
            for (let i = 0; i < correct_btn.length; i++){
                let field = correct_btn[i].parentNode;
                let param = field.parentNode.parentNode.id.split('_')[1];
                console.log(param);
                correct_btn[i].addEventListener("click", () => mark_correct(field, param));
            }
        }
})();