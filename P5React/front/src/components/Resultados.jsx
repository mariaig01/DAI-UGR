import React from 'react';
import Card from 'react-bootstrap/Card';
import Col from 'react-bootstrap/Col';
import Row from 'react-bootstrap/Row';
import Button from 'react-bootstrap/Button';
import { Rating } from 'primereact/rating';

export default function Resultados({ productos }) {
  const cardStyle = {
    width: '400px', 
    height: '500px', 
    objectFit: 'cover',
    border: '1.8px solid #e8e0ca',
    
  };
  const bodyStyle = {
    maxHeight: '200px',
    overflowY: 'scroll',
  };
  const rowStyle = {
    marginTop: '50px',
    flexDirection: 'row',
  };

  return (
    <Row xs={1} sm={1} md={1} lg={3} xl={3} className="g-4" style={rowStyle}>
      {productos.map((producto) => (
        <Col key={producto.id} className="mb-4">
          <Card style={cardStyle} >
            <Card.Img variant="top" src={`${producto.image}`} style={{ maxWidth: '100%', height: '200px' }} alt="..." />
            <Card.Body style={bodyStyle}>
              <Card.Title>{producto.title}</Card.Title>
              <Card.Text>{producto.description}</Card.Text>
              <div className="d-flex justify-content-center align-items-center">
                <Rating value={producto.rating.rate} readOnly cancel={false} />
              </div>
              <div className="d-flex justify-content-center align-items-center">
                <p>Rating: {producto.rating.rate} ({producto.rating.count} votes)</p>
              </div>
            </Card.Body>
            <Card.Footer className="d-flex justify-content-between align-items-center">
              <Button variant="primary" style={{ backgroundColor: 'green', color: 'white', borderColor: 'green' }}>Buy</Button>
              <p className="m-0">{producto.price} €</p>
            </Card.Footer>
          </Card>
        </Col>
      ))}
    </Row>
  );
}
