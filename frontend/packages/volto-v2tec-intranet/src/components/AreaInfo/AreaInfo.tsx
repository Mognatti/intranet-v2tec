import React from 'react';
import { Container } from '@plone/components';
import Icon from '@plone/volto/components/theme/Icon/Icon';
import enterpriseIcon from '@plone/volto/icons/enterprise.svg';
import type { RelatedItem } from '@plone/types';

interface AreaInfoProps {
  content: RelatedItem;
  icon?: boolean;
}

const AreaInfo: React.FC<AreaInfoProps> = ({ content, icon = false }) => {
  return (
    <Container narrow className="areaInfo">
      {icon && (
        <Icon name={enterpriseIcon} size="64px" className="icon listitem" />
      )}
      <Container className="info" narrow>
        <h2 className="title">{content.title}</h2>
        <p className="description">{content.description}</p>
      </Container>
    </Container>
  );
};

export default AreaInfo;
