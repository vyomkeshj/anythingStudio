import { SearchIcon } from '@chakra-ui/icons';
import {
    Accordion,
    AccordionItem,
    Box,
    Button,
    Center,
    ExpandedIndex,
    Icon,
    Input,
    InputGroup,
    InputLeftElement,
} from '@chakra-ui/react';
import { ChangeEventHandler, memo, useMemo, useState } from 'react';
import { BsCaretDownFill, BsCaretUpFill } from 'react-icons/bs';
import { useContext, useContextSelector } from 'use-context-selector';
import { BackendContext } from '../../contexts/BackendContext';
import { DependencyContext } from '../../contexts/DependencyContext';
import { SettingsContext } from '../../contexts/SettingsContext';
import HeaderUI from "../../components/Header";
import {
    getMatchingNodes,
    getNodesByCategory,
    getSubcategories,
    sortSchemata,
} from '../../helpers/nodeSearchFuncs';
import { useNodeFavorites } from '../../hooks/useNodeFavorites';
import { FavoritesAccordionItem } from './FavoritesAccordionItem';
import { PackageHint, RegularAccordionItem, Subcategories } from './RegularAccordionItem';
import { TextBox } from './TextBox';



interface SearchBarProps {
    value: string;
    onChange: ChangeEventHandler<HTMLInputElement>;
    onClose: () => void;
    onClick: () => void;
    onFocusCapture: (status: Boolean) => void;
}

export const SearchBar = memo(({ value, onChange, onClose, onClick, onFocusCapture }: SearchBarProps) => (
    <InputGroup style={{
        "webkitAppRegion":"no-drag" // DON'T REMOVE! ignore the error it will just work
    }}>
    <InputLeftElement
    color="var(--fg-300)"
    pointerEvents="none"
    >
    <SearchIcon />
    </InputLeftElement>
    <Input
    border=".5px solid var(--off-white)"
    placeholder="Ex: connect to jekins"
    textAlign={"center"}
    fontSize={14}
    colorScheme={'blackAlpha'}
    spellCheck={false}
    type="text"
    value={value}
    variant="pill"
    onBlur={() => onFocusCapture(false)}
    onFocusCapture={() => onFocusCapture(true)}
    onChange={onChange}
    onClick={onClick}
    />
    </InputGroup>
    ));

export const NodeSelector = memo(() => {
    const { schemata, categories, categoriesMissingNodes } = useContext(BackendContext);
    const { openDependencyManager } = useContext(DependencyContext);
    const { useExperimentalFeatures } = useContext(SettingsContext);
    const [isExperimentalFeatures] = useExperimentalFeatures;
    
    const [searchQuery, setSearchQuery] = useState('');
    
    const matchingNodes = getMatchingNodes(
        searchQuery,
        sortSchemata(schemata.schemata.filter((s) => !s.deprecated))
        );
        const byCategories = useMemo(() => getNodesByCategory(matchingNodes), [matchingNodes]);
        
        const [collapsed, setCollapsed] = useContextSelector(
            SettingsContext,
            (c) => c.useNodeSelectorCollapsed
            );
            
            const { favorites } = useNodeFavorites();
            const favoriteNodes = useMemo(() => {
                return [...byCategories.values()].flat().filter((n) => favorites.has(n.schemaId));
            }, [byCategories, favorites]);
            
            const [showCollapseButtons, setShowCollapseButtons] = useState(false);
            
            const defaultIndex = Array.from({ length: byCategories.size + 1 }, (_, i) => i);
            const [accordionIndex, setAccordionIndex] = useState<ExpandedIndex>(defaultIndex);
            
            const accordionIsCollapsed = typeof accordionIndex !== 'number' && accordionIndex.length === 0;
            
            const toggleAccordion = () => {
                if (accordionIsCollapsed) {
                    setAccordionIndex(defaultIndex);
                } else {
                    setAccordionIndex([]);
                }
            };

            const [searchFocus, setSearchFocus] = useState(false);
            
            return (
                <Box
                style={{
                    "webkitAppRegion":"no-drag" // DON'T REMOVE! ignore the error it will just work
                }}
                width="100%"
                borderRadius={5}
                bg="var(--node-selector-bg)"
                >
                
                <SearchBar
                value={searchQuery}
                onFocusCapture={(status: Boolean) => setSearchFocus(status)}
                onChange={(e) => {
                    setSearchQuery(e.target.value);
                    setCollapsed(false);
                }}
                onClick={() => setCollapsed(false)}
                onClose={() => setSearchQuery('')}
                />
                <Box
                h="50vh"
                w="32.67%"
                marginTop="3px"
                borderRadius="5px"
                boxShadow={"rgba(0, 0, 0, 0.24) 0px 3px 8px"}
                background={"#3b3b3b"}
                display= {searchFocus ? "block" : "none"}
                zIndex={99999999}
                position="absolute"
                overflowX="hidden"
                overflowY="scroll"
                >
                <Center>
                <Button
                _hover={{
                    bg: 'var(--bg-600)',
                    opacity: 1,
                }}
                aria-label="Collapse/Expand Categories"
                bg="var(--bg-700)"
                // borderRadius="0px 0px 8px 8px"
                h="0.5rem"
                opacity={showCollapseButtons ? 0.75 : 0}
                position="absolute"
                top="154px"
                w={collapsed ? 'auto' : '100px'}
                zIndex={999}
                onClick={toggleAccordion}
                >
                <Icon
                h="14px"
                pt="2px"
                w="20px"
                >
                {accordionIsCollapsed ? (
                    <BsCaretDownFill />
                    ) : (
                        <BsCaretUpFill />
                        )}
                        </Icon>
                        </Button>
                        </Center>
                        <Accordion
                        allowMultiple
                        defaultIndex={defaultIndex}
                        index={accordionIndex}
                        onChange={(event) => setAccordionIndex(event)}
                        >
                        <FavoritesAccordionItem
                        collapsed={collapsed}
                        favoriteNodes={favoriteNodes}
                        noFavorites={favorites.size === 0}
                        />
                        {categories.map((category) => {
                            const categoryNodes = byCategories.get(category.name);
                            const categoryIsMissingNodes =
                            categoriesMissingNodes.includes(category.name);
                            
                            if (!categoryNodes && !categoryIsMissingNodes) {
                                return null;
                            }
                            
                            const subcategoryMap = categoryNodes
                            ? getSubcategories(categoryNodes)
                            : null;
                            
                            return (
                                <RegularAccordionItem
                                category={category}
                                collapsed={collapsed}
                                key={category.name}
                                >
                                {categoryIsMissingNodes && (
                                    <PackageHint
                                    collapsed={collapsed}
                                    hint={category.installHint ?? ''}
                                    packageName={category.name}
                                    onClick={openDependencyManager}
                                    />
                                    )}
                                    {subcategoryMap && (
                                        <Subcategories
                                        collapsed={collapsed}
                                        subcategoryMap={subcategoryMap}
                                        />
                                        )}
                                        </RegularAccordionItem>
                                        );
                                    })}
                                    <AccordionItem>
                                    <Box p={4}>
                                    <TextBox
                                    collapsed={collapsed}
                                    text="pippity pip?"
                                    toolTip={
                                        collapsed
                                        ? 'pippity pip'
                                        : ''
                                    }
                                    onClick={() => {
                                        console.log("this event");
                                        openDependencyManager()
                                    }}
                                    />
                                    </Box>
                                    </AccordionItem>
                                    </Accordion>
                                    </Box>
                                    </Box>
                                    );
                                });
                                