import React from 'react';
import type { PriorityBadgeProps } from '../types';

const styles: Record<PriorityBadgeProps['priority'], string> = {
  CRITICAL: 'border-red-500/50 bg-red-950/60 text-red-200',
  HIGH: 'border-amber-500/50 bg-amber-950/50 text-amber-200',
  MEDIUM: 'border-yellow-500/40 bg-yellow-950/30 text-yellow-100',
  LOW: 'border-sky-500/40 bg-sky-950/40 text-sky-200',
};

const dots: Record<PriorityBadgeProps['priority'], string> = {
  CRITICAL: 'bg-red-400',
  HIGH: 'bg-amber-400',
  MEDIUM: 'bg-yellow-300',
  LOW: 'bg-sky-400',
};

const PriorityBadge: React.FC<PriorityBadgeProps> = ({ priority }) => {
  return (
    <span className={['inline-flex items-center border px-2.5 py-1 font-mono text-xs font-semibold', styles[priority]].join(' ')}>
      <span className={['mr-2 h-1.5 w-1.5', dots[priority]].join(' ')} />
      {priority}
    </span>
  );
};

export default PriorityBadge;
