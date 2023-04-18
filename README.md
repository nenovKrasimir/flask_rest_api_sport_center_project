<h1 align="center">Sport Center Project</h1>
<p align="center">Thats my first basic FLASK REST API
Its oriented in sports managing, buying subscriptions, buying equipments with small logic for delivering part.
The project have authentication part, authorization part and free access part. The authentication part is for admin users which can edit/add/delete 
delivery guys and coaches.
  The part with authorization gives acces for the buying parts.</p>
<h1 align="center">Built with</h1>
<div align="center">

  <p>
    <a href="https://www.python.org/" target="_blank"><img src="https://img.shields.io/badge/Python-3.9-blue?style=flat-square&logo=python" alt="Python"></a>
    <a href="https://flask.palletsprojects.com/" target="_blank"><img src="https://img.shields.io/badge/Flask-2.0.2-blue?style=flat-square&logo=flask" alt="Flask"></a>
    <a href="https://flask-restful.readthedocs.io/en/latest/" target="_blank"><img src="https://img.shields.io/badge/Flask--Restful-0.3.9-blue?style=flat-square" alt="Flask-RESTful"></a>
    <a href="https://flask-migrate.readthedocs.io/en/latest/" target="_blank"><img src="https://img.shields.io/badge/Flask--Migrate-3.1.0-blue?style=flat-square" alt="Flask-Migrate"></a>
    <a href="https://marshmallow.readthedocs.io/en/stable/" target="_blank"><img src="https://img.shields.io/badge/Marshmallow-3.14.1-blue?style=flat-square" alt="Marshmallow"></a>
  </p>
</div>
</p>
<h2>Endpoints:</h2>
<div style="text-align: center;">
    <table>
  <tr>
    <th>Endpoint</th>
    <th>HTTP Method</th>
    <th>Description</th>
  </tr>
  <tr>
    <td>/sports</td>
    <td>GET</td>
    <td>Get all sports</td>
  </tr>
  <tr>
    <td>/sports/{id}</td>
    <td>GET</td>
    <td>Get sport by id</td>
  </tr>
  <tr>
    <td>/sports</td>
    <td>POST</td>
    <td>Create a new sport</td>
  </tr>
  <tr>
    <td>/sports/{id}</td>
    <td>PUT</td>
    <td>Update a sport by id</td>
  </tr>
  <tr>
    <td>/sports/{id}</td>
    <td>DELETE</td>
    <td>Delete a sport by id</td>
  </tr>
  <tr>
    <td>/subscriptions</td>
    <td>GET</td>
    <td>Get all subscriptions</td>
  </tr>
  <tr>
    <td>/subscriptions/{id}</td>
    <td>GET</td>
    <td>Get subscription by id</td>
  </tr>
  <tr>
    <td>/subscriptions</td>
    <td>POST</td>
    <td>Create a new subscription</td>
  </tr>
  <tr>
    <td>/subscriptions/{id}</td>
    <td>PUT</td>
    <td>Update a subscription by id</td>
  </tr>
  <tr>
    <td>/subscriptions/{id}</td>
    <td>DELETE</td>
    <td>Delete a subscription by id</td>
  </tr>
  <tr>
    <td>/equipments</td>
    <td>GET</td>
    <td>Get all equipments</td>
  </tr>
  <tr>
    <td>/equipments/{id}</td>
    <td>GET</td>
    <td>Get equipment by id</td>
  </tr>
  <tr>
    <td>/equipments</td>
    <td>POST</td>
    <td>Create a new equipment</td>
  </tr>
  <tr>
    <td>/equipments/{id}</td>
    <td>PUT</td>
    <td>Update an equipment by id</td>
  </tr>
  <tr>
    <td>/equipments/{id}</td>
    <td>DELETE</td>
    <td>Delete an equipment by id</td>
  </tr>
  <tr>
    <td>/deliveries</td>
    <td>GET</td>
    <td>Get all deliveries</td>
  </tr>
  <tr>
    <td>/deliveries/{id}</td>
    <td>GET</td>
    <td>Get delivery by id</td>
  </tr>
  <tr>
    <td>/deliveries</td>
    <td>POST</td>
    <td>Create a new delivery</td>
  </tr>
  <tr>
    <td>/deliveries/{id}</td>
    <td>PUT</td>
    <td>Update a delivery by id</td>
  </tr>
  <tr>
    <td>/deliveries/{id}</td>
    <td
        <div align="center">
</table>
