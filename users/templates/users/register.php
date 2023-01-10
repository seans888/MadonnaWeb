{%extends "master2.php"%}



<h3>Register here</h3>
<hr>

<form action="" method="POST">
    {% csrf_token %}

    {% for field in form %}
        <div>
            <p>{{ field.label }}: <br> {{ field}}</p>

            {% for error in field.errors %}
                <small style="color: red">{{ error}}</small>
            {% endfor %}
        </div>
    {% endfor %}
    <button type="submit">Register</button>
</form>