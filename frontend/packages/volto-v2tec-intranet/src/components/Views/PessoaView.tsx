import React from 'react';
import { Container } from '@plone/components';
import UniversalLink from '@plone/volto/components/manage/UniversalLink/UniversalLink';
import { flattenToAppURL } from '@plone/volto/helpers/Url/Url';
import type { Pessoa } from 'volto-v2tec-intranet/types/content';
import ContactInfo from 'volto-v2tec-intranet/components/ContactInfo/ContactInfo';
import AddressInfo from 'volto-v2tec-intranet/components/AddressInfo/AddressInfo';
import AreaInfo from 'volto-v2tec-intranet/components/AreaInfo/AreaInfo';

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
        <div className="pessoa-info">
          <div className="pessoa-titulo">
            <h1 className="documentFirstHeading">{title}</h1>
            {content.categoria && (
              <span
                className={`categoria categoria-${content.categoria.token}`}
              >
                {content.categoria.title}
              </span>
            )}
          </div>
          {description && <p className="documentDescription">{description}</p>}
        </div>
      </Container>
      <ContactInfo content={content} />
      <AddressInfo content={content} />
      {content.area && (
        <UniversalLink href={flattenToAppURL(content.area['@id'])}>
          <AreaInfo content={content.area} />
        </UniversalLink>
      )}
    </Container>
  );
};

export default PessoaView;
