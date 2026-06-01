import React from 'react';
import { Container } from '@plone/components';
import type { Area } from 'volto-v2tec-intranet/types/content';

interface AddressInfoProps {
  content: Area;
}

const AddressInfo: React.FC<AddressInfoProps> = ({ content }) => {
  const { endereco, complemento, cidade, estado, cep } = content;

  if (!endereco && !complemento && !cidade && !estado && !cep) {
    return null;
  }

  return (
    <Container narrow className="endereco">
      {endereco && (
        <Container className="endereco-linha">
          <span className="label">Endereço</span>:
          <span className="value">{endereco}</span>
        </Container>
      )}
      {complemento && (
        <Container className="endereco-linha">
          <span className="label">Complemento</span>:
          <span className="value">{complemento}</span>
        </Container>
      )}
      {cidade && (
        <Container className="endereco-linha">
          <span className="label">Cidade</span>:
          <span className="value">{cidade}</span>
        </Container>
      )}
      {estado && (
        <Container className="endereco-linha">
          <span className="label">Estado</span>:
          <span className="value">{estado.title ?? estado.token}</span>
        </Container>
      )}
      {cep && (
        <Container className="endereco-linha">
          <span className="label">CEP</span>:
          <span className="value">{cep}</span>
        </Container>
      )}
    </Container>
  );
};

export default AddressInfo;
