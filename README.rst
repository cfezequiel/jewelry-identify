=======================================================
Jewelry Identification from Images
=======================================================

App that demonstrates how to identify specific jewelry items using computer vision. 

Jewelry company, Pandora Philippines, was looking for a way to quickly inventory the items in their store. However, they did not want to put price tags on any of their jewelry as it would distract the potential customer. The current method involved manually inspecting each item and matching it against a list of available items to get a count. This took a lot of time and effort and is prone to error. 

The proposed solution involved developing a mobile app that can take a snapshot of an item or set of items, and inventory them using computer vision techniques. This allowed one to quickly inventory a set of items without having to manually refer to a lookup table to determine the product ID of any item.

This demo takes an image of a set of jewelry items, segments it into smaller tile images (where each image contains one piece of jewelry), and then tries to match each tile to a database of jewelry images.

This demo was coded in Python and uses the Open-CV Python library.