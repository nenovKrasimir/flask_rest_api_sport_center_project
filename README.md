<h1 align="center">Sport Center Project</h1>
<p align="center">Thats my first basic FLASK REST API
Its oriented in sports managing, buying subscriptions, buying equipments with small logic for delivering part.
The project have authentication part, authorization part and free access part. The authorized part is for admin users which can edit/add/delete 
delivery guys and coaches.We have basic SES AWS service for sending an email for verification upon registration and Stripe payment provider for creating subscriptions and buying products.
<h1 align="center">Setting up Environment and Installing Requirements</h1>

<h5 align="center">
<li>Clone the repository to your local machine using the following command</li>
<pre><code>git clone https://github.com/nenovKrasimir/SportCenterProject.git</code></pre>

<li>Create a virtual environment for your project, you can use the `venv` module in Python. For a detailed guide on how to use `venv`, check out this <a href="https://docs.python.org/3/library/venv.html" target="_blank">step-by-step tutorial
</a>.</li>
 <li>
 Install the required packages by running the following command in the terminal:
    <pre><code>pip install -r requirements.txt</code></pre>
  </li>
  
  <li>Now you're ready to run the application. In the terminal, run the following command:
    <pre><code>python main.py</code></pre>
    The application should now be running at http://localhost:5000.
  </li>
<h1 align="center">Built with


  <p>
    <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-3.9-blue?style=flat-square&logo=python" alt="Python"></a>
    <a href="https://flask.palletsprojects.com/" target="_blank"><img src="https://img.shields.io/badge/Flask-2.0.2-blue?style=flat-square&logo=flask" alt="Flask"></a>
    <a href="https://flask-restful.readthedocs.io/en/latest/" target="_blank"><img src="https://img.shields.io/badge/Flask--Restful-0.3.9-blue?style=flat-square" alt="Flask-RESTful"></a>
    <a href="https://flask-migrate.readthedocs.io/en/latest/" target="_blank"><img src="https://img.shields.io/badge/Flask--Migrate-3.1.0-blue?style=flat-square" alt="Flask-Migrate"></a>
    <a href="https://marshmallow.readthedocs.io/en/stable/" target="_blank"><img src="https://img.shields.io/badge/Marshmallow-3.14.1-blue?style=flat-square" alt="Marshmallow"></a>
  </p>
</div>
</p></h1>
<div style="text-align: center;">
    <table>
 <h1 align="center"       <h2>Endpoints:

<table align="center">
  <tr>
    <th>Endpoint</th>
    <th>HTTP Method</th>
    <th>Description</th>
    <th>Access</th>
  </tr>
  <tr>
    <td>/get_sports
    <td>GET</td>
    <td>Get all sport types</td>
    <td>Free</td>
  </tr>
  <tr>
    <td>/get_products
    <td>GET</td>
    <td>Get all products</td>
    <td>Free</td>
  </tr>
  <tr>
    <td>/registration
    <td>POST</td>
    <td>Create registration</td>
    <td>Free</td>
  </tr>
  <tr>
    <td>/verify_email/<token></td>
    <td>GET</td>
    <td>Verify email</td>
    <td>Free</td>
  </tr>
  <tr>
    <td>/login</td>
    <td>GET</td>
    <td>Login user</td>
    <td>Authentication</td>
  </tr>
  <tr>
    <td>/buy_equipment</td>
    <td>POST</td>
    <td>Buy sport equipment</td>
    <td>Authentication</td>
  </tr>
  <tr>
    <td>/buy_subscriptions</td>
    <td>POST</td>
    <td>Create a new subscription</td>
    <td>Authentication</td>
  </tr>
    <tr>
    <td>/new_access_token</td>
    <td>GET</td>
    <td>Get new access token</td>
    <td>Authentication</td>
  </tr>
  <tr>
    <td>/subscriptions/{id}</td>
    <td>PUT</td>
    <td>Update a subscription by id</td>
    <td>Authentication</td>
  </tr>
  <tr>
    <td>/coach_panel</td>
    <td>GET</td>
    <td>Get all coaches</td>
    <td>Authorization</td>
  </tr>
  <tr>
    <td>/coach_panel</td>
    <td>DELETE</td>
    <td>Delete a coach</td>
    <td>Authorization</td>
  </tr>
  <tr>
    <td>/coach_panel</td>
    <td>POST</td>
    <td>Add coach</td>
    <td>Authorization</td>
  </tr>
  <tr>
    <td>/coach_panel</td>
    <td>PUT</td>
    <td>Update coach contacts</td>
    <td>Authorization</td>
  </tr>
  <tr>
    <td>/delivery_guys_panel</td>
    <td>GET</td>
    <td>Show all delivery guys</td>
    <td>Authorization</td>
  </tr>
  <tr>
    <td>/delivery_guys_panel</td>
    <td>POST</td>
    <td>Add a delivery guy</td>
    <td>Authorization</td>
  </tr>
  <tr>
    <td>/delivery_guys_panel</td>
    <td>PUT</td>
    <td>Update delivery guy contact</td>
    <td>Authorization</td>
  </tr>
    </table>


