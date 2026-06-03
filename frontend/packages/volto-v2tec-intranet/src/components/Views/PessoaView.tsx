import React from 'react';
import { Container } from '@plone/components';
import type { Pessoa } from 'volto-v2tec-intranet/types/content';
import ContactInfo from 'volto-v2tec-intranet/components/ContactInfo/ContactInfo';
import AddressInfo from 'volto-v2tec-intranet/components/AddressInfo/AddressInfo';

interface PessoaViewProps {
  content: Pessoa;
  [key: string]: any;
}

const PessoaView: React.FC<PessoaViewProps> = ({ content }) => {
  const { title, description, image } = content;
  const previewScale = image?.scales?.preview;
  const imageUrl = previewScale?.download ?? image?.download;

  return (
    <Container id="page-document" className="view-wrapper pessoa-view">
      <Container narrow className="pessoa-header">
        {imageUrl && (
          <img
            src={imageUrl}
            alt={title}
            className="pessoa-foto"
            width={previewScale?.width ?? image?.width}
            height={previewScale?.height ?? image?.height}
          />
        )}
        <h1 className="documentFirstHeading">{title}</h1>
        {description && <p className="documentDescription">{description}</p>}
      </Container>
      <ContactInfo content={content} />
      <AddressInfo content={content} />
    </Container>
  );
};

export default PessoaView;
