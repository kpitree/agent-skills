---
name: kpitree-tree-builder
description: Creating, extending, reshaping and cloning KPI trees in KPI Tree. Use when someone asks to build a tree for a topic, add or remove metrics from a tree, change how metrics roll up, or give every site, region or product line the same tree.
---

# Building and editing KPI trees

Tree editing needs the editor role. Where a tool refuses on role, say so and offer the
read-only view instead.

## Start from the catalogue

- `list_trees`: the tree catalogue, with node and edge counts but not the graph.
- `get_tree`: one tree's full structure, nodes and edges.
- `search_metrics`: find the metrics to put in the tree. Filters combine with AND: free
  text, `dimension_value`, `entity`, `owner`, `tree`. `get_metric` for one metric's full
  detail, `get_metric_relationships` for its parents, children and tree memberships.

## Build

1. `search_metrics` to find the metrics for the topic, and `get_metric_relationships` to
   see which relationships already exist.
2. `create_tree` with the metrics; then `add_metric_to_tree` and
   `remove_metric_from_tree` to adjust membership.
3. `update_tree_edges` to set how metrics roll up. Mapped edges are what
   `get_metric_drivers` reports as the strongest evidence, so only draw an edge the
   organisation believes.
4. `rename_tree`, and `rename_group` for the canvas groups a tree is organised into.
   Canvas groups are NOT directory groups (`list_user_groups`) and NOT a person's team or
   department; never merge the three.

## One tree per segment

`clone_tree_for_dimension` copies a tree's whole structure onto another dimension value,
so every site, region or product line gets an identically shaped tree. Reach for it
rather than rebuilding a tree per segment by hand. It refuses rather than build a
partial tree, and names the metrics that have no counterpart; resolve those first
(`explore_entity` shows a dimension's values).

## Linking trees

`link_tree_node` and `unlink_tree_node` (child_trees feature): a linked node points at
another tree, so a company tree can link out to per-segment trees. Navigation only;
nothing rolls up through a link.

Before any edit, say what will change and confirm with the person. After the edit,
read the tree back with `get_tree` and describe it by name, never by UUID.
