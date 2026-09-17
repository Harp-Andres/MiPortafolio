/**
 * Portfolio project types
 */

export interface Project {
  id: string;
  name: string;
  description: string;
  longDescription: string;
  technologies: string[];
  github: string;
  link?: string;
  highlights: string[];
  type: 'featured' | 'secondary' | 'supporting';
  image?: string;
  stats?: {
    stars?: number;
    watchers?: number;
    forks?: number;
  };
}
