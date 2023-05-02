import React, { memo } from 'react'
import usePropsSelector from "../../../../hooks/usePropsSelector";
import SizeControl from "../../controls/SizeControl";
import ColorsControl from "../../controls/ColorsControl";
import SwitchControl from "../../controls/SwitchControl";
import VariantsControl from "../../controls/VariantsControl";

const IconButtonPanel = () => {
  const size = usePropsSelector('size')
  const variant = usePropsSelector('variant')

  return (
    <>
      {/*<IconControl name="icon" label="Icon" />*/}
      <SizeControl name="size" label="Size" value={size} />
      <ColorsControl label="Color" name="colorScheme" />
      <SwitchControl label="Loading" name="isLoading" />
      <SwitchControl label="Round" name="isRound" />
      <VariantsControl label="Variant" name="variant" value={variant} />
    </>
  )
}

export default memo(IconButtonPanel)
