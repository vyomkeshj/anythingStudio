import React, { memo } from 'react'
import { Accordion } from '@chakra-ui/react'
import EffectsPanel from './styles/EffectsPanel'
import CustomPropsPanel from './CustomPropsPanel'
import PaddingPanel from "./styles/PaddingPanel";
import ParentInspector from "../ParentInspector";
import ChildrenInspector from "../ChildrenInspector";
import AccordionContainer from "../AccordionContainer";
import DisplayPanel from "./styles/DisplayPanel";
import DimensionPanel from "./styles/DimensionPanel";
import TextPanel from "./styles/TextPanel";
import ColorsControl from "../controls/ColorsControl";
import GradientControl from "../controls/GradientControl";
import BorderPanel from "./styles/BorderPanel";

interface Props {
  isRoot: boolean
  showChildren: boolean
  parentIsRoot: boolean
}

const StylesPanel: React.FC<Props> = ({
  isRoot,
  showChildren,
  parentIsRoot,
}) => (
  <Accordion defaultIndex={[0]} allowMultiple>
    {!isRoot && (
      <AccordionContainer title="Custom props">
        <CustomPropsPanel />
      </AccordionContainer>
    )}

    {!isRoot && !parentIsRoot && (
      <AccordionContainer title="Parent">
        <ParentInspector />
      </AccordionContainer>
    )}

    {showChildren && (
      <AccordionContainer title="Children">
        <ChildrenInspector />
      </AccordionContainer>
    )}

    {!isRoot && (
      <>
        <AccordionContainer title="Layout">
          <DisplayPanel />
        </AccordionContainer>
        <AccordionContainer title="Spacing">
          <PaddingPanel type="margin" />
          <PaddingPanel type="padding" />
        </AccordionContainer>
        <AccordionContainer title="Size">
          <DimensionPanel />
        </AccordionContainer>
        <AccordionContainer title="Typography">
          <TextPanel />
        </AccordionContainer>
      </>
    )}

    <AccordionContainer title="Backgrounds">
      <ColorsControl
        withFullColor
        label="Color"
        name="backgroundColor"
        enableHues
      />
      {!isRoot && (
        <GradientControl
          withFullColor
          label="Gradient"
          name="bgGradient"
          options={[
            'to top',
            'to top right',
            'to top left',
            'to bottom right',
            'to bottom',
            'to bottom left',
            'to right',
            'to left',
          ]}
          enableHues
        />
      )}
    </AccordionContainer>

    {!isRoot && (
      <>
        <AccordionContainer title="Border">
          <BorderPanel />
        </AccordionContainer>

        <AccordionContainer title="Effect">
          <EffectsPanel />
        </AccordionContainer>
      </>
    )}
  </Accordion>
)

export default memo(StylesPanel)
