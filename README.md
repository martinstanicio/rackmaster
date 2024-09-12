# RackMaster

**RackMaster** is a simplified Warehouse Management System (WMS) designed to efficiently organize and manage products in a warehouse using a custom coordinate system. This system helps optimize product storage, retrieval, and internal movements within the warehouse, ensuring that workers can minimize walking distance while retrieving items.

## Features

### Inbound Operations

Allows users to input product codes, quantities, and the coordinates where the items will be stored. Prevents possible conflicts, such as trying to store two different items in the same position.

### Outbound Operations

Facilitates product retrieval by providing an optimized route based on product coordinates, ensuring the shortest path is taken, and updates inventory based on product withdrawal.

### Internal Movement or Swap

Supports the movement of items from one position to another, or swapping items between two positions.

## Coordinate System

The warehouse uses a custom coordinate system to define storage locations:

- `XX`: Rack-block row number.
- `YYY`: Position within the row (each rack contains 3 pallets, and each pallet is divided into 3 sections, so there are 9 possible positions in a single rack).
- `ZZ`: Level or height within the rack.

Example coordinate: `(50, 002, 01)` (Rack-block 50, Position 002, Level 01).
