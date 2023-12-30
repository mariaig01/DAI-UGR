import React from 'react';
import Card from 'react-bootstrap/Card';
import CardGroup from 'react-bootstrap/CardGroup';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import { Rating } from 'primereact/rating';

export default function Results({ productos }) {
  return (
    <Row xs={1} sm={1} md={2} lg={3} xl={4} className="g-4">
      {productos.map((producto) => (
        <Col key={producto.id}>
          <Card>
            <Card.Body>
              <Card.Title>{producto.title}</Card.Title>
              <Card.Text>{producto.description}</Card.Text>
            </Card.Body>
            <div className="d-flex justify-content-center align-items-center">
              <Rating value={producto.rating.rate} readOnly cancel={false} />
            </div>
            <div className="d-flex justify-content-center align-items-center">
              <p></p>
            </div>
            <Card.Footer className="d-flex justify-content-between align-items-center">
              <Button variant="primary">Comprar</Button>
              <p className="m-0">{producto.price} €</p>
            </Card.Footer>
          </Card>
        </Col>
      ))}
    </Row>
  );
}