import React from 'react';
import { Container } from '@plone/components';
import { flattenToAppURL } from '@plone/volto/helpers/Url/Url';
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
      {content.area && (
        <Container narrow className="area-wrapper">
          <span className="label">Área</span>:{' '}
          <a href={flattenToAppURL(content.area['@id'])}>
            {content.area.title}
          </a>
        </Container>
      )}
      {content.categoria && (
        <Container narrow className="categoria-wrapper">
          <span className={`categoria categoria-${content.categoria.token}`}>
            {content.categoria.title}
          </span>
        </Container>
      )}
    </Container>
  );
};

export default PessoaView;
