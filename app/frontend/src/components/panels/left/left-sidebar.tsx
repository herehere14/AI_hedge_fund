// left-sidebar.tsx - Modern Block.inc inspired design

import { useFlowManagementTabs } from '@/hooks/use-flow-management-tabs';
import { useResizable } from '@/hooks/use-resizable';
import { cn } from '@/lib/utils';
import { ReactNode, useEffect } from 'react';
import { FlowActions } from './flow-actions';
import { FlowCreateDialog } from './flow-create-dialog';
import { FlowList } from './flow-list';

interface LeftSidebarProps {
  children?: ReactNode;
  isCollapsed: boolean;
  onCollapse: () => void;
  onExpand: () => void;
  onToggleCollapse: () => void;
  onWidthChange?: (width: number) => void;
}

export function LeftSidebar({
  isCollapsed,
  onToggleCollapse,
  onWidthChange,
}: LeftSidebarProps) {
  // Use our custom hooks
  const { width, isDragging, elementRef, startResize } = useResizable({
    defaultWidth: 280,
    minWidth: 240,
    maxWidth: 480,
    side: 'left',
  });

  // Notify parent component of width changes
  useEffect(() => {
    onWidthChange?.(width);
  }, [width, onWidthChange]);
  
  // Use flow management hook with tabs
  const {
    flows,
    searchQuery,
    isLoading,
    openGroups,
    createDialogOpen,
    filteredFlows,
    recentFlows,
    templateFlows,
    setSearchQuery,
    setCreateDialogOpen,
    handleAccordionChange,
    handleCreateNewFlow,
    handleFlowCreated,
    handleSaveCurrentFlow,
    handleOpenFlowInTab,
    handleDeleteFlow,
    handleRefresh,
  } = useFlowManagementTabs();

  return (
    <div 
      ref={elementRef}
      className={cn(
        "h-full bg-card/95 backdrop-blur-sm flex flex-col relative",
        "border-r border-border/50 shadow-xl",
        isCollapsed ? "shadow-2xl" : "",
        isDragging ? "select-none" : "",
        "panel-transition"
      )}
      style={{ 
        width: `${width}px`
      }}
    >
      {/* Modern header section */}
      <div className="p-4 border-b border-border/50 bg-background/50">
        <h2 className="text-sm font-semibold text-foreground mb-3">Flows</h2>
        <FlowActions
          onSave={handleSaveCurrentFlow}
          onCreate={handleCreateNewFlow}
          onToggleCollapse={onToggleCollapse}
        />
      </div>
      
      <FlowList
        flows={flows}
        searchQuery={searchQuery}
        isLoading={isLoading}
        openGroups={openGroups}
        filteredFlows={filteredFlows}
        recentFlows={recentFlows}
        templateFlows={templateFlows}
        onSearchChange={setSearchQuery}
        onAccordionChange={handleAccordionChange}
        onLoadFlow={handleOpenFlowInTab}
        onDeleteFlow={handleDeleteFlow}
        onRefresh={handleRefresh}
      />
      
      {/* Modern resize handle */}
      {!isDragging && (
        <div 
          className="absolute top-0 right-0 h-full w-1 cursor-ew-resize 
                     transition-all duration-150 z-10 hover:w-1.5 
                     hover:bg-primary/30 active:bg-primary/50"
          onMouseDown={startResize}
        />
      )}

      <FlowCreateDialog
        isOpen={createDialogOpen}
        onClose={() => setCreateDialogOpen(false)}
        onFlowCreated={handleFlowCreated}
      />
    </div>
  );
}