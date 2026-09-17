import {
  Hero,
  About,
  Skills,
  Experience,
  Education,
  Certificates,
} from '@/components'
import { CV_DATA } from '@/utils/cv-data'

interface HomeProps {
  onDownloadATS: () => void
  onDownloadVisual: () => void
}

export const Home = (_props: HomeProps) => {
  return (
    <main>
      <Hero name={CV_DATA.name} title={CV_DATA.title} />
      <About
        email={CV_DATA.email}
        phone={`${CV_DATA.phone1} - ${CV_DATA.phone2}`}
        location={CV_DATA.location}
        linkedin={CV_DATA.linkedin}
        birthDate={CV_DATA.birthDate}
        about={CV_DATA.profile}
      />
      <Skills categories={CV_DATA.skills} />
      <Experience items={CV_DATA.experience} />
      <Education items={CV_DATA.education} />
      <Certificates 
        byCategory={CV_DATA.certificatesByCategory}
        learningPaths={CV_DATA.learningPathsCertifications}
        officialCertifications={CV_DATA.officialCertifications}
        items={CV_DATA.certificates}
      />
    </main>
  )
}
