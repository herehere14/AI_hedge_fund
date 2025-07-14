// right-sidebar.tsx - Modern Block.inc inspired design

import { ComponentGroup, getComponentGroups } from '@/data/sidebar-components';
import { useComponentGroups } from '@/hooks/use-component-groups';
import { useResizable } from '@/hooks/use-resizable';
import { cn } from '@/lib/utils';
import { ReactNode, useEffect, useState } from 'react';
import { ComponentActions } from './component-actions';
import { ComponentList } from './component-list';

interface RightSidebarProps {
  children?: ReactNode;
  isCollapsed: boolean;
  onCollapse: () => void;
  onExpand: () => void;
  onToggleCollapse: () => void;
  onWidthChange?: (width: number) => void;
}

export function RightSidebar({
  isCollapsed,
  onToggleCollapse,
  onWidthChange,
}: RightSidebarProps) {
  // Use our custom hooks
  const { width, isDragging, elementRef, startResize } = useResizable({
    defaultWidth: 280,
    minWidth: 240,
    maxWidth: 480,
    side: 'right',
  });
  
  // Notify parent component of width changes
  useEffect(() => {
    onWidthChange?.(width);
  }, [width, onWidthChange]);
  
  // State for loading component groups
  const [componentGroups, setComponentGroups] = useState<ComponentGroup[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  
  // Load component groups on mount
  useEffect(() => {
    const loadComponentGroups = async () => {
      try {
        setIsLoading(true);
        const groups = await getComponentGroups();
        setComponentGroups(groups);
      } catch (error) {
        console.error('Failed to load component groups:', error);
      } finally {
        setIsLoading(false);
      }
    };
    
    loadComponentGroups();
  }, []);
  
  const { 
    searchQuery, 
    setSearchQuery, 
    activeItem, 
    openGroups, 
    filteredGroups,
    handleAccordionChange 
  } = useComponentGroups(componentGroups);

  return (
    <div 
      ref={elementRef}
      className={cn(
        "h-full bg-card/95 backdrop-blur-sm flex flex-col relative",
        "border-l border-border/50 shadow-xl",
        isCollapsed ? "shadow-2xl" : "",
        isDragging ? "select-none" : "",
        "panel-transition"
      )}
      style={{ 
        width: `${width}px`,
      }}
    >
      {/* Modern header section */}
      <div className="p-4 border-b border-border/50 bg-background/50">
        <h2 className="text-sm font-semibold text-foreground mb-3">Components</h2>
        <ComponentActions onToggleCollapse={onToggleCollapse} />
      </div>
      
      <ComponentList
        componentGroups={componentGroups}
        searchQuery={searchQuery}
        isLoading={isLoading}
        openGroups={openGroups}
        filteredGroups={filteredGroups}
        activeItem={activeItem}
        onSearchChange={setSearchQuery}
        onAccordionChange={handleAccordionChange}
      />
      
      {/* Modern resize handle */}
      {!isDragging && (
        <div 
          className="absolute top-0 left-0 h-full w-1 cursor-ew-resize 
                     transition-all duration-150 z-10 hover:w-1.5 
                     hover:bg-primary/30 active:bg-primary/50"
          onMouseDown={startResize}
        />
      )}
    </div>
  );
}