class_<VisionBlackboard>("VisionBlackboard")
   .add_property("balls"    , &VisionBlackboard::balls    )
   .add_property("timestamp", &VisionBlackboard::timestamp)
   .add_property("robots"   , &VisionBlackboard::robots);
   // .add_property("refereeHands", &VisionBlackboard::refereeHands);
